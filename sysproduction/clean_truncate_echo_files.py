from sysdata.data_blob import dataBlob
from syscore.fileutils import (
    delete_old_files_with_extension_in_pathname,
    rename_files_with_extension_in_pathname_as_archive,
)

from sysproduction.data.directories import get_echo_file_directory, get_echo_extension


def clean_truncate_echo_files():
    data = dataBlob()
    cleaner = cleanTruncateEchoFiles(data)
    cleaner.clean_echo_files()
    return None


class cleanTruncateEchoFiles:
    def __init__(self, data: dataBlob):
        self.data = data

    def clean_echo_files(self):
        pathname = get_echo_file_directory()
        echo_extension = get_echo_extension()
        self.data.log.msg("Archiving echo files")
        rename_files_with_extension_in_pathname_as_archive(
            pathname, extension=echo_extension, new_extension=".arch"
        )
        self.data.log.msg("Deleting old echo files")
        delete_old_files_with_extension_in_pathname(
            pathname, extension=".arch", days_old=30
        )


