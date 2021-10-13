import os
from datetime import datetime
from error_logging.utils import error_logger

def split(filehandler,
          delimiter: str,
          row_limit: int,
          output_name_template: str,
          output_path: str,
          keep_headers: bool,
          format_for_upload: bool):
    """
    Splits a CSV file into multiple pieces.

    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:

        >> from toolbox import csv_splitter;
        >> breakout_funcs.utils.split(open('C:/ADD_CVD/input.csv', 'r'));

    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
    current_limit = row_limit
    date = datetime.today().strftime('%Y_%m_%d')
    line_1 = ['PRODUCT_CSV', 'ADD_OR_REPLACE', f'{date}', 'ISO-8859-1']
    headers = next(reader)
    if format_for_upload:
        current_out_writer.writerow(line_1)
        error_logger.info(f"writing {line_1} to {current_out_path}")
    if keep_headers:
        current_out_writer.writerow(headers)
        error_logger.info(f"writing {headers} to {current_out_path}")
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
            if format_for_upload:
                current_out_writer.writerow(line_1)
                error_logger.info(f"writing {line_1} to {current_out_path}")
            if keep_headers:
                current_out_writer.writerow(headers)
                error_logger.info(f"writing {headers} to {current_out_path}")
        current_out_writer.writerow(row)
