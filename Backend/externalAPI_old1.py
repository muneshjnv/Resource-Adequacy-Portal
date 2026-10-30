"""
External REST API — Demand Forecast Portal
==========================================
This module provides a public read-only API for external consumers who are
NOT users of the portal itself.

Authentication : X-API-Key header  (keys stored in api_keys table)
Base prefix    : /api/v1/
Versioning     : v1

Endpoints
---------
GET /api/v1/states                  — List all states (state_id, state_name, acronym)
GET /api/v1/forecast                — Forecast data for all states on a given date
    ?type=day|intraday|week|month|year
    ?date=YYYY-MM-DD                — For day/intraday : the forecast date
                                    — For week/month/year : any date falling within
                                      the forecast period (e.g., the start date)

How to register this Blueprint in dFBackend.py
-----------------------------------------------
    from externalAPI import external_api
    app.register_blueprint(external_api)
"""

import secrets
import psycopg2
from functools import wraps
from datetime import datetime, date

import json
from flask import Blueprint, request, jsonify, Response
from collections import OrderedDict

# ─────────────────────────────────────────────
# Blueprint
# ─────────────────────────────────────────────
external_api = Blueprint("external_api", __name__)

# ─────────────────────────────────────────────
# Database helpers
# ─────────────────────────────────────────────
DB_PARAMS = {
    "dbname":   "demand_forecast_states",
    "user":     "ra_admin",
    "password": "admin",
    "host":     "localhost",
    "port":     "5432",
}


def get_db():
    """Return a fresh psycopg2 connection + cursor."""
    conn = psycopg2.connect(**DB_PARAMS)
    return conn, conn.cursor()


# ─────────────────────────────────────────────
# Column definitions per forecast type
# ─────────────────────────────────────────────

DAY_INTRA_COLUMNS = [
    "block_no",
    "time_period",
    "forecasted_demand_mw",
    "thermal_mw",
    "gas_mw",
    "hydro_mw",
    "total_own_sources_mw",
    "solar_mw",
    "wind_mw",
    "other_res_mw",
    "total_renewable_mw",
    "isgs_lta_mtoa_mw",
    "bilateral_advance_fcfs_mw",
    "total_availability_mw",
    "gap_surplus_deficit_mw",
    "procurement_bilateral_mw",
    "procurement_exchange_mw",
    "shortage_after_procurement_mw",
    "relief_restrictions_mw",
    "additional_load_shedding_mw",
    "reactive_power_mvar",
    # --- new columns in the updated format (cols 22-37) ---
    "secondary_up_ancillary_mw",
    "secondary_down_ancillary_mw",
    "tertiary_up_ancillary_mw",
    "tertiary_down_ancillary_mw",
    "ur_s_plant1_mw",
    "ur_s_plant2_mw",
    "ur_s_plant3_mw",
    "ur_t_plant1_mw",
    "ur_t_plant2_mw",
    "ur_t_plant3_mw",
    "dr_s_plant1_mw",
    "dr_s_plant2_mw",
    "dr_s_plant3_mw",
    "dr_t_plant1_mw",
    "dr_t_plant2_mw",
    "dr_t_plant3_mw",
]

WEEK_MONTH_YEAR_COLUMNS = [
    "date",
    "block_no",
    "time_period",
    "forecasted_demand_mw",
    "thermal_mw",
    "gas_mw",
    "hydro_mw",
    "total_own_sources_mw",
    "solar_mw",
    "wind_mw",
    "other_res_mw",
    "total_renewable_mw",
    "isgs_lta_mtoa_mw",
    "bilateral_advance_fcfs_mw",
    "total_availability_mw",
    "gap_surplus_deficit_mw",
    "procurement_bilateral_mw",
    "procurement_exchange_mw",
    "shortage_after_procurement_mw",
    "relief_restrictions_mw",
    "additional_load_shedding_mw",
    "reactive_power_mvar",
]


def row_to_dict(columns, row):
    """Zip a column list with a data row, skipping extra cells gracefully."""
    return {columns[i]: (row[i] if i < len(row) else None) for i in range(len(columns))}


def _nest_block_row(row: dict) -> dict:
    """Map a flat record to the exact block structure requested by the user."""
    # helpers to safely read numeric values
    def n(k):
        v = row.get(k)
        return v if isinstance(v, (int, float)) else (float(v) if v is not None and str(v).replace('.', '', 1).lstrip('-').isdigit() else 0.0)

    # compute 'Others' inside own sources if total provided
    thermal = n("thermal_mw")
    gas = n("gas_mw")
    hydro = n("hydro_mw")
    total_own = n("total_own_sources_mw")
    others_own = total_own - (thermal + gas + hydro)
    if others_own < 0:
        others_own = 0.0

    solar = n("solar_mw")
    wind = n("wind_mw")
    other_res = n("other_res_mw")
    total_renew = n("total_renewable_mw")

    block = OrderedDict()
    block["Time"] = OrderedDict([
        ("Block", row.get("block_no")),
        ("Period", row.get("time_period"))
    ])

    block["Forcasted Generation/Availability"] = OrderedDict([
        ("Forcasted Demand (A)", n("forecasted_demand_mw")),
        ("From its own sources (excluding Renewable)", OrderedDict([
            ("Thermal (Coal + Lignite)", thermal),
            ("Gas", gas),
            ("Hydro", hydro),
            ("Others", round(others_own, 6)),
            ("Total (B)", total_own)
        ])),
        ("From Renewable Sources", OrderedDict([
            ("Solar", solar),
            ("Wind", wind),
            ("Other RES (biomass etc.)", other_res),
            ("Total (C)", total_renew)
        ])),
        ("From ISGS & Other LTA & MTOA (D)", n("isgs_lta_mtoa_mw")),
        ("From Bilateral Transaction (Advance+ FCFS) (E)", n("bilateral_advance_fcfs_mw")),
        ("Total Availability (F)= (B+C+D+E)", n("total_availability_mw")),
    ])

    block["Gap between Demand & Availability (G) = (A)-(F) Surplus(-) / Deficit (+)"] = n("gap_surplus_deficit_mw")

    block["Proposed Procurement"] = OrderedDict([
        ("Under Bilateral Transaction (Day Ahead+ Exigency) (H)", n("procurement_bilateral_mw")),
        ("Through Power Exchange (I)", n("procurement_exchange_mw"))
    ])

    # J: gap after procurement (shortage_after_procurement_mw)
    j_val = n("shortage_after_procurement_mw")
    block["Gap after day ahead procurement from market (J) =(G)-(H+I) Surplus(-) / Deficit (+)"] = j_val
    block["Relief through planned restrictions/ rostering/ power cuts (K)"] = n("relief_restrictions_mw")

    # L: either provided or compute
    l_val = n("additional_load_shedding_mw")
    if l_val == 0.0:
        l_val = max(0.0, j_val - n("relief_restrictions_mw"))
    block["Gap after shedding proposed (L) = (J)-(K) Surplus(-) / Deficit (+)"] = l_val

    block["Reactive Power Forecast"] = n("reactive_power_mvar")

    block["Up Reserve"] = OrderedDict([
        ("Secondary", n("secondary_up_ancillary_mw")),
        ("Tertiary", n("tertiary_up_ancillary_mw"))
    ])
    block["Down Reserve"] = OrderedDict([
        ("Secondary", n("secondary_down_ancillary_mw")),
        ("Tertiary", n("tertiary_down_ancillary_mw"))
    ])

    # Details of Reserves - plant-wise allocations
    drs = [n("dr_s_plant1_mw"), n("dr_s_plant2_mw"), n("dr_s_plant3_mw")]
    drt = [n("dr_t_plant1_mw"), n("dr_t_plant2_mw"), n("dr_t_plant3_mw")]
    urs = [n("ur_s_plant1_mw"), n("ur_s_plant2_mw"), n("ur_s_plant3_mw")]
    urt = [n("ur_t_plant1_mw"), n("ur_t_plant2_mw"), n("ur_t_plant3_mw")]

    details = OrderedDict()
    details["Plant-wise allocation of UR_S"] = OrderedDict([
        ("Plant-1", urs[0]),
        ("Plant-2", urs[1])
    ])
    details["Plant-wise allocation of UR_T"] = OrderedDict([
        ("Plant-1", urt[0]),
        ("Plant-2", urt[1])
    ])
    details["Plant-wise allocation of DR_S"] = OrderedDict([
        ("Plant-1", drs[0]),
        ("Plant-2", drs[1])
    ])
    details["Plant-wise allocation of DR_T"] = OrderedDict([
        ("Plant-1", drt[0]),
        ("Plant-2", drt[1])
    ])

    block["Details of Reserves"] = details

    return block


def _compute_total_lus(records: list) -> dict:
    """Compute totals and return a mapping matching the "Total LUs" section in the sample.

    The function sums numeric fields across all provided flat records and returns
    an OrderedDict with human-readable labels used in the required JSON.
    """
    def sum_key(k):
        s = 0.0
        for r in records:
            v = r.get(k)
            if isinstance(v, (int, float)):
                s += v
            else:
                try:
                    s += float(v)
                except Exception:
                    pass
        return s

    total_A = sum_key("forecasted_demand_mw")
    total_B = sum_key("total_own_sources_mw")
    total_C = sum_key("total_renewable_mw")
    total_D = sum_key("isgs_lta_mtoa_mw")
    total_E = sum_key("bilateral_advance_fcfs_mw")
    total_F = sum_key("total_availability_mw")
    total_G = sum_key("gap_surplus_deficit_mw")
    total_H = sum_key("procurement_bilateral_mw")
    total_I = sum_key("procurement_exchange_mw")
    total_J = sum_key("shortage_after_procurement_mw")
    total_K = sum_key("relief_restrictions_mw")
    # L: gap after shedding proposed — use additional_load_shedding_mw if present, else compute J-K
    total_L = sum_key("additional_load_shedding_mw")
    if total_L == 0.0:
        total_L = max(0.0, total_J - total_K)

    totals = OrderedDict([
        ("Forcasted Demand (A)", total_A),
        ("Total (B)", total_B),
        ("Total (C)", total_C),
        ("From ISGS & Other LTA & MTOA (D)", total_D),
        ("From Bilateral Transaction (Advance+ FCFS) (E)", total_E),
        ("Total Availability (F)= (B+C+D+E)", total_F),
        ("Gap between Demand & Availability (G) = (A)-(F) Surplus(-) / Deficit (+)", total_G),
        ("Under Bilateral Transaction (Day Ahead+ Exigency) (H)", total_H),
        ("Through Power Exchange (I)", total_I),
        ("Gap after day ahead procurement from market (J) =(G)-(H+I) Surplus(-) / Deficit (+)", total_J),
        ("Relief through planned restrictions/ rostering/ power cuts (K)", total_K),
        ("Gap after shedding proposed (L) = (J)-(K) Surplus(-) / Deficit (+)", total_L),
    ])

    return totals


# ─────────────────────────────────────────────
# API Key authentication decorator
# ─────────────────────────────────────────────

def require_api_key(f):
    """
    Decorator that validates the X-API-Key request header against the
    api_keys table.  Returns 401 if the key is missing, invalid, inactive,
    or expired.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({
                "status": "error",
                "error":  "Missing API key. Pass your key in the X-API-Key header."
            }), 401

        try:
            conn, cursor = get_db()
            # print("a")
            cursor.execute(
                """
                SELECT owner_name, is_active
                FROM   api_keys
                WHERE  api_key = %s
                """,
                (api_key,)
            )
            # print("b")
            row = cursor.fetchone()

            cursor.close()
            conn.close()
        except Exception as e:
            return jsonify({"status": "error", "error": "Database error during key validation"}), 500

        if not row:
            return jsonify({"status": "error", "error": "Invalid API key"}), 401

        owner_name, is_active = row

        if not is_active:
            return jsonify({"status": "error", "error": "API key has been revoked"}), 401


        # Attach owner info to request context for logging (optional)
        request.api_key_owner = owner_name
        return f(*args, **kwargs)

    return decorated


# ─────────────────────────────────────────────
# Helper: fetch all states
# ─────────────────────────────────────────────

def fetch_all_states():
    """Return list of dicts: [{state_id, state_name, acronym}, ...]"""
    conn, cursor = get_db()
    cursor.execute("SELECT state_id, state_name, acronym FROM states ORDER BY state_id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"state_id": r[0], "state_name": r[1], "acronym": r[2]} for r in rows]


# ─────────────────────────────────────────────
# Endpoint 1 — GET /api/v1/states
# ─────────────────────────────────────────────

@external_api.route("/api/v1/states", methods=["GET"])
@require_api_key
def list_states():
    """
    Return all states with their IDs and names.

    Example:
        GET /api/v1/states
        X-API-Key: <your-key>
    """
    try:
        states = fetch_all_states()
        return jsonify({
            "status":  "success",
            "count":   len(states),
            "states":  states
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ─────────────────────────────────────────────
# Endpoint 2 — GET /api/v1/forecast
# ─────────────────────────────────────────────

@external_api.route("/api/v1/forecast", methods=["GET"])
@require_api_key
def get_forecast():
    """
    Fetch the latest-revision forecast data for ALL states.

    Query Parameters
    ----------------
    type        : str  — one of: day | intraday | week | month | year  (required)

    For type = day | intraday:
        date    : str  — YYYY-MM-DD  (required) — the exact forecast date

    For type = week | month | year:
        from_date : str  — YYYY-MM-DD  (required) — start of the forecast period
        to_date   : str  — YYYY-MM-DD  (required) — end   of the forecast period

    Response
    --------
    {
      "status":    "success",
      "type":      "day",
      "date":      "2024-06-01",           # present for day / intraday
      "from_date": "2024-06-03",           # present for week / month / year
      "to_date":   "2024-06-09",           # present for week / month / year
      "generated": "2024-06-18T10:30:00Z",
      "count":     8,
      "data": [
        {
          "state_id":    5,
          "state_name":  "West Bengal",
          "acronym":     "WB",
          "upload_time": "2024-06-01T08:45:00",
          "revision_no": 1,
          "record_count": 96,
          "records": [
            { "block_no": 1, "time_period": "00:00-00:15", "forecasted_demand_mw": 3450.5 }
          ]
        }
      ]
    }
    """
    # ── Validate type ────────────────────────────────────────────────────
    forecast_type = (request.args.get("type") or "").strip().lower()
    VALID_TYPES   = {"day", "intraday", "week", "month", "year"}
    PERIOD_TYPES  = {"week", "month", "year"}
    SINGLE_TYPES  = {"day", "intraday"}

    if not forecast_type:
        return jsonify({"status": "error",
                        "error": "Missing required parameter: type. "
                                 "Allowed values: day | intraday | week | month | year"}), 400

    if forecast_type not in VALID_TYPES:
        return jsonify({"status": "error",
                        "error": f"Invalid type '{forecast_type}'. "
                                 f"Allowed values: {', '.join(sorted(VALID_TYPES))}"}), 400

    # ── Parse state filter ──────────────────────────────────────────────
    state_param = (request.args.get("state") or "").strip()
    state_filter = None
    if state_param:
        state_map = _get_state_map()
        state_filter = [sid for sid, info in state_map.items()
                        if state_param.lower() == info["state_name"].lower()
                        or state_param.lower() == info["acronym"].lower()
                        or state_param == str(sid)]
        if not state_filter:
            return jsonify({"status": "error", "error": f"State not found: {state_param}"}), 404

    # ── Parse date parameters based on type ─────────────────────────────
    if forecast_type in SINGLE_TYPES:
        # day / intraday — single date
        date_str = (request.args.get("date") or "").strip()
        if not date_str:
            return jsonify({"status": "error",
                            "error": f"Missing required parameter: date (format: YYYY-MM-DD) "
                                     f"for type='{forecast_type}'"}), 400
        try:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"status": "error",
                            "error": "Invalid date format. Use YYYY-MM-DD (e.g. 2024-06-01)"}), 400
    else:
        date_str = None

        # week / month / year — date range
        from_date_str = (request.args.get("from_date") or "").strip()
        to_date_str   = (request.args.get("to_date")   or "").strip()

        if not from_date_str:
            return jsonify({"status": "error",
                            "error": f"Missing required parameter: from_date (format: YYYY-MM-DD) "
                                     f"for type='{forecast_type}'"}), 400
        if not to_date_str:
            return jsonify({"status": "error",
                            "error": f"Missing required parameter: to_date (format: YYYY-MM-DD) "
                                     f"for type='{forecast_type}'"}), 400
        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
            to_date   = datetime.strptime(to_date_str,   "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"status": "error",
                            "error": "Invalid date format. Use YYYY-MM-DD (e.g. 2024-06-03)"}), 400

        if from_date > to_date:
            return jsonify({"status": "error",
                            "error": "from_date must be on or before to_date"}), 400

    # ── Route to correct fetcher ─────────────────────────────────────────
    try:
        if forecast_type == "day":
            result_data = _fetch_day_or_intra("file_uploads", query_date, state_filter)
        elif forecast_type == "intraday":
            result_data = _fetch_day_or_intra("intraday_file_uploads", query_date, state_filter)
        elif forecast_type == "week":
            result_data = _fetch_period("week_ahead_file_uploads", from_date, to_date, state_filter)
        elif forecast_type == "month":
            result_data = _fetch_period("month_ahead_file_uploads", from_date, to_date, state_filter)
        elif forecast_type == "year":
            result_data = _fetch_period("year_ahead_file_uploads", from_date, to_date, state_filter)
    except Exception as e:
        return jsonify({"status": "error", "error": f"Database error: {str(e)}"}), 500

    if not result_data:
        response_payload = {
            "status":  "success",
            "type":    forecast_type,
            "generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z",
            "count":   0,
            "data":    []
        }
        if forecast_type in SINGLE_TYPES:
            response_payload["date"] = date_str
        else:
            response_payload["from_date"] = from_date_str
            response_payload["to_date"] = to_date_str
        return jsonify(response_payload), 200

    # If caller requested a specific state and only one result found,
    # return that state object directly (no wrapper) to match exact schema.
    state_param = (request.args.get("state") or "").strip()
    if state_param and result_data and len(result_data) == 1:
        return Response(json.dumps(result_data[0], ensure_ascii=False, default=str, sort_keys=False), mimetype="application/json"), 200

    # Build an ordered response payload and dump JSON without sorting keys.
    response_payload = OrderedDict()
    response_payload["status"] = "success"
    response_payload["type"] = forecast_type
    if forecast_type in SINGLE_TYPES:
        response_payload["date"] = date_str
    else:
        response_payload["from_date"] = from_date_str
        response_payload["to_date"] = to_date_str
    response_payload["generated"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    response_payload["count"] = len(result_data)
    response_payload["data"] = result_data

    return Response(json.dumps(response_payload, ensure_ascii=False, default=str, sort_keys=False), mimetype="application/json"), 200


# ─────────────────────────────────────────────
# Internal helpers — data fetchers
# ─────────────────────────────────────────────

def _get_state_map():
    """Return {state_id: {state_name, acronym}} for all states."""
    conn, cursor = get_db()
    cursor.execute("SELECT state_id, state_name, acronym FROM states")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {r[0]: {"state_name": r[1], "acronym": r[2]} for r in rows}


def _fetch_day_or_intra(table: str, query_date: date, state_filter: list | None = None) -> list:
    """
    Fetch the latest revision for every state from file_uploads or
    intraday_file_uploads for a specific upload_date.

    Returns a list of state-level dicts, each containing the block records.
    """
    conn, cursor = get_db()
    state_map = _get_state_map()

    # Latest revision per state for the given date
    query = f"""
        SELECT DISTINCT ON (state_id)
               state_id,
               upload_time,
               revision_no,
               file_data
        FROM   {table}
        WHERE  upload_date = %s
        ORDER  BY state_id, revision_no DESC, upload_time DESC
    """
    cursor.execute(query, (query_date,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    results = []
    for state_id, upload_time, revision_no, file_data in rows:
        if state_filter is not None and state_id not in state_filter:
            continue

        info = state_map.get(state_id, {"state_name": "Unknown", "acronym": ""})

        # file_data is a list of rows from JSONB
        records = []
        blocks = []
        for row in (file_data or []):
            block_no = row[0] if row else None
            if not isinstance(block_no, (int, float)):
                continue
            record = row_to_dict(DAY_INTRA_COLUMNS, row)
            records.append(record)
            blocks.append(_nest_block_row(record))

        state_entry = OrderedDict()
        state_entry["Details for State:"] = info["state_name"]
        state_entry["For Date:"] = query_date.strftime("%d-%b-%y")
        state_entry["Blocks"] = blocks
        state_entry["Total LUs"] = _compute_total_lus(records)
        results.append(state_entry)

    return results


def _fetch_period(table: str, from_date: date, to_date: date, state_filter: list | None = None) -> list:
    """
    Fetch the latest revision for every state from week/month/year ahead tables
    where the stored forecast period falls within [from_date, to_date].

    Matching logic: stored from_date >= param from_date
                AND stored to_date   <= param to_date
    This returns records whose entire period is contained within the
    requested range (e.g. the exact week/month/year the user asked for).

    Returns a list of state-level dicts, each containing the block records.
    """
    conn, cursor = get_db()
    state_map = _get_state_map()

    query = f"""
        SELECT DISTINCT ON (state_id)
               state_id,
               from_date,
               to_date,
               upload_time,
               revision_no,
               file_data
        FROM   {table}
        WHERE  from_date >= %s AND to_date <= %s
        ORDER  BY state_id, revision_no DESC, upload_time DESC
    """
    cursor.execute(query, (from_date, to_date))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    results = []
    for state_id, from_date, to_date, upload_time, revision_no, file_data in rows:
        if state_filter is not None and state_id not in state_filter:
            continue

        info = state_map.get(state_id, {"state_name": "Unknown", "acronym": ""})

        records = []
        blocks = []
        for row in (file_data or []):
            if not row:
                continue
            first = row[0]
            if isinstance(first, str) and not _looks_like_date(first):
                continue
            record = row_to_dict(WEEK_MONTH_YEAR_COLUMNS, row)
            records.append(record)
            blocks.append(_nest_block_row(record))

        state_entry = OrderedDict()
        state_entry["Details for State:"] = info["state_name"]
        state_entry["For Date:"] = f"{from_date.strftime('%d-%b-%y')} to {to_date.strftime('%d-%b-%y')}"
        state_entry["Blocks"] = blocks
        state_entry["Total LUs"] = _compute_total_lus(records)
        results.append(state_entry)

    return results


def _looks_like_date(s: str) -> bool:
    """Quick check: does this string look like a date (not a column header)?"""
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d-%b-%Y"):
        try:
            datetime.strptime(s, fmt)
            return True
        except ValueError:
            pass
    return False


# ─────────────────────────────────────────────
# Admin Endpoint — Generate a new API key
# (Protected by a one-time admin secret passed in header)
# ─────────────────────────────────────────────

@external_api.route("/api/v1/admin/generate-key", methods=["POST"])
def generate_api_key():
    """
    Generate and store a new API key.
    Protected by X-Admin-Secret header (set ADMIN_SECRET below).

    Request Body (JSON):
    {
        "owner_name": "Organization Name",
    }

    Response:
    {
        "status": "success",
        "api_key": "<generated-key>",
        "owner_name": "Organization Name",

    }
    """
    # ── Admin secret check ───────────────────────────────────────────────
    # Change this to a strong secret and store it securely (env var in production)
    ADMIN_SECRET = "ERLDC_Admin"

    admin_secret = request.headers.get("X-Admin-Secret")
    if not admin_secret or admin_secret != ADMIN_SECRET:
        return jsonify({"status": "error", "error": "Unauthorized"}), 401

    body = request.get_json() or {}
    owner_name = body.get("owner_name", "").strip()

    if not owner_name:
        return jsonify({"status": "error", "error": "owner_name is required"}), 400



    # Generate a cryptographically secure API key
    new_key = "dfp_" + secrets.token_urlsafe(32)  # e.g.  dfp_abc123...

    try:
        conn, cursor = get_db()
        cursor.execute(
            """
            INSERT INTO api_keys (api_key, owner_name, is_active, created_at)
            VALUES (%s, %s, TRUE, NOW())
            """,
            (new_key, owner_name)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "error": f"Database error: {str(e)}"}), 500

    return jsonify({
        "status":     "success",
        "api_key":    new_key,
        "owner_name": owner_name,

    }), 201


# ─────────────────────────────────────────────
# Admin Endpoint — Revoke an API key
# ─────────────────────────────────────────────

@external_api.route("/api/v1/admin/revoke-key", methods=["POST"])
def revoke_api_key():
    """
    Revoke (deactivate) an existing API key.
    Protected by X-Admin-Secret header.

    Request Body (JSON):
    { "api_key": "<key-to-revoke>" }
    """
    ADMIN_SECRET = "ERLDC_Admin"

    admin_secret = request.headers.get("X-Admin-Secret")
    if not admin_secret or admin_secret != ADMIN_SECRET:
        return jsonify({"status": "error", "error": "Unauthorized"}), 401

    body = request.get_json() or {}
    key_to_revoke = body.get("api_key", "").strip()

    if not key_to_revoke:
        return jsonify({"status": "error", "error": "api_key is required"}), 400

    try:
        conn, cursor = get_db()
        cursor.execute(
            "UPDATE api_keys SET is_active = FALSE WHERE api_key = %s",
            (key_to_revoke,)
        )
        updated = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "error": f"Database error: {str(e)}"}), 500

    if updated == 0:
        return jsonify({"status": "error", "error": "API key not found"}), 404

    return jsonify({"status": "success", "message": "API key revoked successfully"}), 200
