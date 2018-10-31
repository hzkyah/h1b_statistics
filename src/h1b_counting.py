import loader as data_loader
import max_heap as max_heap

config = {}
aggregate_states = {}
aggregate_jobs = {}
job_titles = {}


# callback method for loading input data
def process_data(chunk, eof):
    if not eof:  # check if end of file reached
        for row in chunk:
            line = row.split(config['field_separator'])
            if not line[0].isdigit():  # only done for the first row of field name vs index identification
                header = {k: v for v, k in enumerate(line)}
                config['case_index'] = ([header[name] for name in config['case_names'] if name in header])[0]
                config['job_index'] = [header[name] for name in config['job_codes'] if name in header][0]
                config['site_index'] = [header[name] for name in config['site_names'] if name in header][0]
                config['title_index'] = [header[name] for name in config['job_names'] if name in header][0]
                config['total'] = 0
            else:
                if line[config['case_index']] == 'CERTIFIED':
                    config['total'] += 1
                    aggregate_states[line[config['site_index']]] = aggregate_states.get(line[config['site_index']], 0) + 1
                    aggregate_jobs[line[config['job_index']]] = aggregate_jobs.get(line[config['job_index']], 0) + 1
                    job_titles[line[config['job_index']]] = str(line[config['title_index']]).replace('"', '')


# method for pushing to heap
def build_heap(top_heap, aggregates, size, coded):
    for key, value in aggregates.items():
        if coded:
            key = job_titles[key]
        top_heap.push((key, value))

# output to file or console
def output(top_heap, path, header, size):
    with open(path, "w") as file:
        print(header, file=file)
        for i in range(int(size)):
            top = top_heap.pop()
            if top:
                percentage = top[1]/config['total'] * 100
                print(str(top[0]) + ';' + str(top[1]) + ';' + str(round(percentage, 1)) + '%', file=file)


# fill initial configuration parameters from config.txt
def read_configuration(configuration):
    with open(".\/" + "config.txt") as configfile:
        for line in configfile:
            if line[0] == '#':
                continue
            data = line.split('=')
            data[0], data[1] = data[0].strip(), data[1].strip()
            configuration[data[0]] = data[1]
            if data[0] in ['case_names', 'job_codes', 'job_names', 'site_names']:
                configuration[data[0]] = data[1].split(';')


if __name__ == "__main__":

    read_configuration(config)
    path = config['input_path'] + config['input_file_name']
    row_break = config['row_separator']

    # process_data method is the callback method.
    # It will be called for each chunk of lines, with parameter data representing chunk of lines of the file at a time
    data_loader.read_lines_as_chunks(path, row_break, chunk_size=int(config['CHUNK_SIZE']), callback=process_data)

    top_states_heap = max_heap.MaxHeap([])
    top_jobs_heap = max_heap.MaxHeap([])

    build_heap(top_jobs_heap, aggregate_jobs, config['output_size'], coded=True)
    build_heap(top_states_heap, aggregate_states, config['output_size'], coded=False)

    output(top_jobs_heap, config['output_path'] + config['output_1'], config['output_1_header'], config['output_size'])
    output(top_states_heap, config['output_path'] + config['output_2'], config['output_2_header'], config['output_size'])
