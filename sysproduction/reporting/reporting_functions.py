import pandas as pd

from syscore.objects import resolve_function,  arg_not_supplied
from syscore.objects import header, table, body_text

from sysdata.data_blob import dataBlob
from syslogdiag.email_via_db_interface import send_production_mail_msg

from sysproduction.reporting.report_configs import reportConfig

def run_report(report_config: reportConfig,
               data: dataBlob=arg_not_supplied):
    """

    :param report_config:
    :return:
    """
    pandas_display_for_reports()
    if data is arg_not_supplied:
        data = dataBlob(log_name="Reporting %s" % report_config.title)

    run_report_with_data_blob(report_config, data)


def run_report_with_data_blob(report_config: reportConfig,
                              data: dataBlob):
    """

    :param report_config:
    :return:
    """

    data.log.msg("Running report %s" % str(report_config))
    report_function = resolve_function(report_config.function)
    report_kwargs = report_config.kwargs

    report_results = report_function(data, **report_kwargs)
    parsed_report = parse_report_results(report_results)

    # We either print or email
    if report_config.output is "console":
        print(parsed_report)
    elif report_config.output is "email":
        send_production_mail_msg(
            data, parsed_report, subject=report_config.title, email_is_report=True
        )




def parse_report_results(report_results: list):
    """
    Parse report results into human readable text for display, email, or christmas present

    :param report_results: list of header, body or table
    :return: String, with more \n than you can shake a stick at
    """
    output_string = ""
    for report_item in report_results:
        if isinstance(report_item, header):
            parsed_item = parse_header(report_item)
        elif isinstance(report_item, body_text):
            parsed_item = parse_body(report_item)
        elif isinstance(report_item, table):
            parsed_item = parse_table(report_item)
        else:
            parsed_item = " %s failed to parse in report\n" % str(report_item)

        output_string = output_string + parsed_item

    return output_string


def parse_table(report_table: table) -> str:
    table_header = report_table.Heading
    table_body = str(report_table.Body)
    table_header_centred = centralise_text(table_header, table_body)
    underline_header = landing_strip_from_str(table_header_centred)

    table_string = "\n%s\n%s\n%s\n\n%s\n\n" % (
        underline_header,
        table_header_centred,
        underline_header,
        table_body,
    )

    return table_string


def parse_body(report_body: body_text) -> str:
    body_text = report_body.Text
    return "%s\n" % body_text


def parse_header(report_header: header) -> str:
    header_line = landing_strip(80, "*")
    header_text = centralise_text(report_header.Heading, header_line)

    return "\n%s\n%s\n%s\n\n\n" % (header_line, header_text, header_line)


def landing_strip_from_str(str_to_match: str, strip: str="=") -> str:
    str_width = measure_width(str_to_match)
    return landing_strip(width=str_width, strip=strip)


def landing_strip(width: int=80, strip: str="*"):
    return strip * width


def centralise_text(text: str, str_to_match: str, pad_with: str=" ") ->str:
    match_len = measure_width(str_to_match)
    text_len = len(text)
    if text_len >= match_len:
        return text
    pad_left = int((match_len - text_len) / 2.0)
    pad_right = match_len - pad_left - text_len
    pad_left_text = pad_with * pad_left
    pad_right_text = pad_with * pad_right

    new_text = "%s%s%s" % (pad_left_text, text, pad_right_text)

    return new_text


def measure_width(text: str) -> int:
    first_cr = text.find("\n")
    if first_cr == -1:
        first_cr = len(text)

    return first_cr


def pandas_display_for_reports():
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_columns", 1000)
    pd.set_option("display.max_rows", 1000)

