# bulky
Bulk rename files and directories

        --options=<options>
Options:

        f                                       Rename files
        d                                       Rename directories
        r                                       Recursive run
        c                                       Capitalize words - Note: This will capitalize everything in path, regardless of the matching.
        i                                       Ignore extensions (in combination with <f>)

        --path=<str>

Operations (output is grouped by allowed combinations):

        --keep-left=<int>                       Keep <int> characters on left
        --keep-right=<int>                      Keep <int> characters on right

        --replace=<str>                         Replace <str>
        --with=<str>                            With <str>
                null => replace with nothing
                space => replace with space

        --insert=<str>                          Insert <str> at start
        --at=<int>                              Insert <str> at <int>
        --append=<str>                          Append <str> to end

        --strip-left=<int>                      Strip <int> characters from start
        --strip-right=<int>                     Strip <int> characters from end

        --file-as-parent=<search_file_name>     rename <search_file_name> to match parent directory name
        --move-up                               Move file un one directory

By default, only task output is displayed - no renaming or moving is done. To perform the actual task, use the production run switch

        --make-it-so                            Do a production run

        --dump                                  Print detected arguments
        --verbose                               Verbose output

Example:

        bulky.py --options=fdi --path=/temp/directory --replace=hello --with=world
        bulky.py --options=fr --path=/temp/directory --keep-left=10 --keep-right=5
        bulky.py --options=fc --path=/temp/directory --strip-left=5 --strip-right=5
        bulky.py --options=f --path=/temp/directory --insert=hello --at=4 --append=world
        bulky.py --path=/temp/directory --file-as-parent=file.ext --move-up --make-it-so
