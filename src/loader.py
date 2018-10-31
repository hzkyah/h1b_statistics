def read_lines_as_chunks(path, row_break, chunk_size, callback, return_whole_chunk=True):

    """
    read file line by line regardless of its size
    :param path: absolute path of file to read
    :param row_break: new line character marking the end of a row
    :param chunk_size: size of data to be read at at time
    :param callback: callback method, prototype ----> def callback(data, eof)
    :param return_whole_chunk: control how to return chunk i.e line by line or group of lines
    """

    def read_in_chunks(file_obj):
        while True:
            data = file_obj.read(chunk_size)
            if not data:
                break
            yield data

    fp = open(path, encoding="utf8")
    data_left_over = None

    # loop through characters
    for chunk in read_in_chunks(fp):
        # if uncompleted data exists
        if data_left_over:
            # print('\n left over found')
            current_chunk = data_left_over + chunk
        else:
            current_chunk = chunk

        # split chunk by new line
        lines = current_chunk.splitlines()
        # check if line is complete
        if current_chunk.endswith(row_break):
            data_left_over = None
        else:
            data_left_over = lines.pop()
        if return_whole_chunk:
            callback(chunk=lines, eof=False)
        else:
            for line in lines:
                callback(chunk=line, eof=False)
                pass

    if data_left_over:
        current_chunk = data_left_over
        if current_chunk is not None:
            lines = current_chunk.splitlines()
            if return_whole_chunk:
                callback(chunk=lines, eof=False)
            else:
                for line in lines:
                    callback(chunk=line, eof=False)
                    pass

    callback(chunk=None, eof=True)
