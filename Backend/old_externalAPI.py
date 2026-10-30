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

from flask import Blueprint, request, jsonify

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
            print(row)
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
            result_data = _fetch_day_or_intra("file_uploads", query_date)
        elif forecast_type == "intraday":
            result_data = _fetch_day_or_intra("intraday_file_uploads", query_date)
        elif forecast_type == "week":
            result_data = _fetch_period("week_ahead_file_uploads", query_date)
        elif forecast_type == "month":
            result_data = _fetch_period("month_ahead_file_uploads", query_date)
        elif forecast_type == "year":
            result_data = _fetch_period("year_ahead_file_uploads", query_date)
    except Exception as e:
        return jsonify({"status": "error", "error": f"Database error: {str(e)}"}), 500

    if not result_data:
        return jsonify({
            "status":  "success",
            "type":    forecast_type,
            "date":    date_str,
            "message": "No data found for the given date and forecast type.",
            "data":    []
        }), 200

    return jsonify({
        "status":    "success",
        "type":      forecast_type,
        "date":      date_str,
        "generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z",
        "count":     len(result_data),
        "data":      result_data
    }), 200


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


def _fetch_day_or_intra(table: str, query_date: date) -> list:
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
        info = state_map.get(state_id, {"state_name": "Unknown", "acronym": ""})

        # file_data is a list of rows from JSONB
        records = []
        for row in (file_data or []):
            # Skip header rows (block_no column is not numeric)
            block_no = row[0] if row else None
            if not isinstance(block_no, (int, float)):
                continue
            records.append(row_to_dict(DAY_INTRA_COLUMNS, row))

        results.append({
            "state_id":    state_id,
            "state_name":  info["state_name"],
            "acronym":     info["acronym"],
            "upload_time": upload_time.isoformat() if upload_time else None,
            "revision_no": revision_no,
            "record_count": len(records),
            "records":     records
        })

    return results


def _fetch_period(table: str, from_date: date, to_date: date) -> list:
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
        info = state_map.get(state_id, {"state_name": "Unknown", "acronym": ""})

        records = []
        for row in (file_data or []):
            # Skip header rows — first cell should be a date string or numeric
            if not row:
                continue
            first = row[0]
            if isinstance(first, str) and not _looks_like_date(first):
                continue
            records.append(row_to_dict(WEEK_MONTH_YEAR_COLUMNS, row))

        results.append({
            "state_id":    state_id,
            "state_name":  info["state_name"],
            "acronym":     info["acronym"],
            "from_date":   from_date.isoformat() if from_date else None,
            "to_date":     to_date.isoformat()   if to_date   else None,
            "upload_time": upload_time.isoformat() if upload_time else None,
            "revision_no": revision_no,
            "record_count": len(records),
            "records":     records
        })

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
