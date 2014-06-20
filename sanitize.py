import unicodedata
import sys


def _are_unicode(unicode_args=[]):
    test_results = [(type(arg) == unicode) for arg in unicode_args]

    if False in test_results:
        return False
    else:
        return True


def sanitize_path_fragment(
        original_fragment,
        filename_extension = u'', # when you do want a filename extension, there is no need to include the leading dot.
        target_file_systems = {'btrfs', 'ext', 'ext2', 'ext3', 'ext3cow', 'ext4', 'exfat', 'fat32', 'hfs+', 'ntfs_win32', 'reiser4', 'reiserfs', 'xfs', 'zfs'},
        sanitization_method = 'underscore',
        truncate = True,
        replacement = u'_',
        additional_illegal_characters=[],):
    if sys.version_info[0] == 2:
        # enforce that these args are unicode strings
        unicode_args = [original_fragment, filename_extension, replacement] + additional_illegal_characters
        if not _are_unicode(unicode_args):
            raise ValueError('`original_fragment`, `filename_extension`, `replacement`, and `additional_illegal_characters` must be of the unicode type under Python 2.')

    sanitized_fragment = unicodedata.normalize('NFC', original_fragment)
    if len(filename_extension) > 0:
        filename_extension = unicodedata.normalize('NFC', u'.' + filename_extension)

    if sanitization_method == 'underscore':
        illegal_characters = {
            'btrfs': {u'\0', u'/'},
            'ext': {u'\0', u'/'},
            'ext2': {u'\0', u'/'},
            'ext3': {u'\0', u'/'},
            'ext3cow': {u'\0', u'/', u'@'},
            'ext4': {u'\0', u'/'},
            'exfat': {
                u'\00', u'\01', u'\02', u'\03', u'\04', u'\05', u'\06', u'\07', u'\10', u'\11', u'\12', u'\13', u'\14', u'\15', u'\16', u'\17',
                u'\20', u'\21', u'\22', u'\23', u'\24', u'\25', u'\26', u'\27', u'\30', u'\31', u'\32', u'\33', u'\34', u'\35', u'\36', u'\37',
                u'/', u'\\', u':', u'*', u'?', u'"', u'<', u'>', u'|',
            },
            'fat32': { # TODO: Confirm this list; current list is just a wild guess, assuming UTF-16 encoding.
                u'\00', u'\01', u'\02', u'\03', u'\04', u'\05', u'\06', u'\07', u'\10', u'\11', u'\12', u'\13', u'\14', u'\15', u'\16', u'\17',
                u'\20', u'\21', u'\22', u'\23', u'\24', u'\25', u'\26', u'\27', u'\30', u'\31', u'\32', u'\33', u'\34', u'\35', u'\36', u'\37',
                u'/', u'\\', u':', u'*', u'?', u'"', u'<', u'>', u'|',
            },
            'hfs+': {u'\0', u'/', u':'}, # In theory, all Unicode characters, including NUL, are usable (HFS+ is awesome in this way); so this is just a sane set for legacy compatibility
            'ntfs_win32': {u'\0', u'/', u'\\', u':', u'*', u'?', u'"', u'<', u'>', u'|'}, # NTFS Win32 namespace (which is stricter)
            'ntfs_posix': {u'\0', u'/'}, # NTFS POSIX namespace (which allows more characters)
            'reiser4': {u'\0', u'/'},
            'reiserfs': {u'\0', u'/'},
            'xfs': {u'\0', u'/'},
            'zfs': {u'\0', u'/'},
            'additional_illegal_characters': set(additional_illegal_characters),
        }
        # Replace illegal characters with an underscore
        for character in set.union(*illegal_characters.values()):
            sanitized_fragment = sanitized_fragment.replace(character, replacement)
            filename_extension = filename_extension.replace(character, replacement)

        # "Quote" illegal filenames
        if target_file_systems.intersection({'fat32', 'ntfs_win32'}):
            windows_reserved_names = (u"CON", u"PRN", u"AUX", u"NUL", u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8",
                                      u"COM9", u"LPT1", u"LPT2", u"LPT3", u"LPT4", u"LPT5", u"LPT6", u"LPT7", u"LPT8", u"LPT9")
            if sanitized_fragment in windows_reserved_names:
                sanitized_fragment = replacement + sanitized_fragment + replacement
            if filename_extension in windows_reserved_names:
                filename_extension = replacement + filename_extension + replacement


        # Truncate if the resulting string is too long
        if truncate:
            max_lengths = {
                # For the entries of file systems commonly found with Linux, the length, 'utf-8', and 'NFC' are only assumptions that apply to mostly vanilla kernels with default build parameters.
                # Seriously, this is 2013. The fact that the Linux community does not move to a file system with an enforced Unicode filename encoding is as bad as Windows 95's codepage madness, some 18 years ago.
                # If you add more file systems, see if it is affected by Unicode Normal Forms, like HFS+; You may have to take extra care in editing the actual sanitization routine below.
                'btrfs': (255, 'bytes', 'utf-8', 'NFC'),
                'ext': (255, 'bytes', 'utf-8', 'NFC'),
                'ext2': (255, 'bytes', 'utf-8', 'NFC'),
                'ext3': (255, 'bytes', 'utf-8', 'NFC'),
                'ext3cow': (255, 'bytes', 'utf-8', 'NFC'),
                'ext4': (255, 'bytes', 'utf-8', 'NFC'),
                'exfat': (255, 'characters', 'utf-16', 'NFC'),
                'fat32': (255, 'characters', 'utf-16', 'NFC'), # 'utf-16' is not entirely true. FAT32 used to be used with codepages; but since Windows XP, the default seems to be UTF-16.
                'hfs+': (255, 'characters', 'utf-16', 'NFD'), # FIXME: improve HFS+ handling, because it does not use the standard NFD. It's close, but it's not exactly the same thing.
                'ntfs_win32': (255, 'characters', 'utf-16', 'NFC'),
                'ntfs_posix': (255, 'characters', 'utf-16', 'NFC'),
                'reiser4': (3976, 'bytes', 'utf-8', 'NFC'), # I don't care if Linux can't support >255 bytes. The adoption of filenames longer than 255 bytes is long overdue.
                'reiserfs': (4032, 'bytes', 'utf-8', 'NFC'), # Same here.
                'xfs': (255, 'bytes', 'utf-8', 'NFC'),
                'zfs': (255, 'bytes', 'utf-8', 'NFC'),
            }
            for file_system in target_file_systems:
                if max_lengths[file_system][1] == 'bytes':
                    extension_bytes = unicodedata.normalize(max_lengths[file_system][3], filename_extension).encode(max_lengths[file_system][2])
                    if sys.version_info[0] == 2:
                        temp_fragment = ''
                    else: # assume Python 3
                        temp_fragment = bytearray()
                    for character in sanitized_fragment:
                        encoded_bytes = unicodedata.normalize(max_lengths[file_system][3], character).encode(max_lengths[file_system][2])
                        if len(temp_fragment) + len(encoded_bytes) + len(extension_bytes)<= max_lengths[file_system][0]:
                            temp_fragment = temp_fragment + encoded_bytes
                        else:
                            break
                    sanitized_fragment = unicodedata.normalize('NFC', temp_fragment.decode(max_lengths[file_system][2]))
                else: # Assume 'characters'
                    temp_fragment = ''
                    if file_system == 'hfs+':
                        normalize = unicodedata.ucd_3_2_0.normalize
                    else:
                        normalize = unicodedata.normalize
                    normalized_extension = normalize(max_lengths[file_system][3], filename_extension)
                    for character in sanitized_fragment:
                        normalized_character = normalize(max_lengths[file_system][3], character)
                        if len(temp_fragment) + len(normalized_character) + len(normalized_extension) <= max_lengths[file_system][0]:
                            temp_fragment += normalized_character
                        else:
                            break
                    sanitized_fragment = unicodedata.normalize('NFC', temp_fragment)

        sanitized_fragment = sanitized_fragment + filename_extension

        # Disallow a final dot or space for FAT32 and NTFS in Win32 namespace.
        # This can only be done after truncations because otherwise we may fix the fragment, but
        # still end up with a bad ending character once it's truncated
        if (
            target_file_systems.intersection({'fat32', 'ntfs_win32'}) and
            (sanitized_fragment.endswith(u".") or sanitized_fragment.endswith(u" "))
        ):
            sanitized_fragment = sanitized_fragment[:-1] + replacement
    else:
        raise ValueError("sanitization_method must be a valid sanitization method")
    return sanitized_fragment
