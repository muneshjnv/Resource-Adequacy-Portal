import * as XLSX from 'xlsx';

export interface ERLDCWorkbookValidationOptions {
  rowsPerDay: number;
  dayCount: number;
  expectedColumns: number;
  blockColumn: number;
  periodColumn?: number;
  lastPeriodEnd?: '00:00' | '24:00';
  demandColumn: number;
  forecastStartColumn: number;
}

const requiredSheets = ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'DVC', 'Sikkim'];
const firstDataRow = 7;

function expectedPeriod(blockNumber: number, rowsPerDay: number, lastPeriodEnd: '00:00' | '24:00'): string {
  const startMinutes = (blockNumber - 1) * 15;
  const endMinutes = blockNumber * 15;
  const formatTime = (minutes: number): string =>
    `${String(Math.floor(minutes / 60) % 24).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;
  const end = blockNumber === rowsPerDay ? lastPeriodEnd : formatTime(endMinutes);
  return `${formatTime(startMinutes)} - ${end}`;
}

export function validateERLDCWorkbook(
  workbook: XLSX.WorkBook,
  options: ERLDCWorkbookValidationOptions
): string | null {
  if (!Number.isInteger(options.dayCount) || options.dayCount <= 0) {
    return 'Please select a complete forecast period before uploading.';
  }

  const sheetNames = new Map(workbook.SheetNames.map(name => [name.trim().toLowerCase(), name]));
  const expectedRows = options.rowsPerDay * options.dayCount;

  for (const requiredSheet of requiredSheets) {
    const sheetName = sheetNames.get(requiredSheet.toLowerCase());
    if (!sheetName) {
      return `The workbook is missing the ${requiredSheet} sheet.`;
    }

    const rows = XLSX.utils.sheet_to_json<unknown[]>(workbook.Sheets[sheetName], {
      header: 1,
      defval: null,
      blankrows: true
    });
    let hasForecastedDemand = false;

    for (let rowIndex = 0; rowIndex < expectedRows; rowIndex++) {
      const row = rows[firstDataRow + rowIndex];
      const blockNumber = (rowIndex % options.rowsPerDay) + 1;
      const period = options.periodColumn === undefined ? undefined : row?.[options.periodColumn];
      if (!row || row.length < options.expectedColumns ||
          Number(row[options.blockColumn]) !== blockNumber ||
          (options.periodColumn !== undefined &&
            (typeof period !== 'string' ||
              period.trim() !== expectedPeriod(blockNumber, options.rowsPerDay, options.lastPeriodEnd ?? '24:00')))) {
        return `${sheetName} does not contain all forecast rows in the required format.`;
      }

      for (let columnIndex = options.forecastStartColumn; columnIndex < options.expectedColumns; columnIndex++) {
        const value = row[columnIndex];
        if (value === null || value === undefined || (typeof value === 'string' && value.trim() === '')) {
          continue;
        }

        const isNumeric = (typeof value === 'number' && Number.isFinite(value)) ||
          (typeof value === 'string' && Number.isFinite(Number(value)));
        if (!isNumeric) {
          return `${sheetName}, row ${rowIndex + 1}: forecast values must be numbers or blank.`;
        }
      }

      const demand = row[options.demandColumn];
      if (demand !== null && demand !== undefined && String(demand).trim() !== '' && Number(demand) !== 0) {
        hasForecastedDemand = true;
      }
    }

    if (!hasForecastedDemand) {
      return `${sheetName}: Forecasted Demand contains all zeroes. Please correct the data.`;
    }
  }

  return null;
}
