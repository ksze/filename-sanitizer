filename-sanitizer
==================

A Python 2.7/3.2+ module that aims to sanitize filenames in a cross-platform, cross-filesystem manner.

Dedicated to Nadia Mahmood, my good friend Jawaad's newborn daughter. Maybe this module will be useful to her if she ever decides to follow her father's footsteps in becoming a hacker. ;-)

This is only a beginning; much work needs to be done to deal with the various filesystems' under-documented aspects.

Unlike most of the extremely naïve, whitelist-based solutions found on the Internet, this solution deals much better with Unicode filenames.

How to use
----------

```py3
    >>> from filename_sanitizer import sanitize_path_fragment
    >>> crazy_filename = u'"foo/bar<bla>yada*meow?.'
    >>> sanitized_filename = sanitize_path_fragment(
    ...     crazy_filename,
    ...     target_file_systems = {'ntfs_win32'},
    ...     replacement = u'-'
    ... )
    ...
    >>> print(sanitized_filename)
    -foo-bar-bla-yada-meow--
    >>>
```

Read the file [`filename_sanitizer/__init__.py`](filename_sanitizer/__init__.py) for details of how the function deals with various file systems.

License
-------

BSD 2-Clause License. See the file [LICENSE](LICENSE).
