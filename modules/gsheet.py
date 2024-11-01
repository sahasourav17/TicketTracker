import gspread
import pandas as pd
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
from requests.exceptions import ConnectionError
import logging
import traceback

logger = logging.getLogger(__name__)


class GSheet:

    def __init__(self, json_filename: str) -> None:
        self.sa = gspread.service_account(
            filename=json_filename)  # type: ignore

    def read_sheet(self, filename: str, sheetname: str = 'Sheet1') -> list[dict] | None:
        try:
            sheets = self.sa.open(filename)
            wsh = sheets.worksheet(sheetname)

            return wsh.get_all_records()
        except SpreadsheetNotFound:
            logger.error(
                'SpreadsheetNotFound: Reading {} + {}'.format(filename, sheetname))
            return []
        except WorksheetNotFound:
            logger.error(
                'WorksheetNotFound: Reading {} + {}'.format(filename, sheetname))
            return []
        except ConnectionError:
            logger.error(
                'ConnectionError: {} + {}'.format(filename, sheetname))
            return self.read_sheet(filename, sheetname)
        except Exception:
            logger.error(traceback.format_exc())

    def update_sheet(self, df: pd.DataFrame, filename: str, sheetname: str, columns=[]) -> None:
        try:
            sheets = self.sa.open(filename)
            try:
                wsh = sheets.worksheet(sheetname)
            except gspread.exceptions.WorksheetNotFound:
                logger.info('Worksheet not found, creating new worksheet {}'.format(sheetname))
                wsh = sheets.add_worksheet(sheetname, rows=100, cols=20)

            if columns:
                df = df[columns]
            df = df.fillna('')

            wsh.clear()
            wsh.update([df.columns.values.tolist()] + df.values.tolist())
        except SpreadsheetNotFound:
            logger.error(
                'Spreadsheet not found: {} + {}'.format(filename, sheetname))
        except Exception:
            logger.error(traceback.format_exc())
