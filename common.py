from collections import OrderedDict
from pyquery import PyQuery
from psycopg2.extensions import adapt


def parse_html(data, key_rename, table_selector):
    query = PyQuery(data)
    columns = OrderedDict()
    rows = list(generate_rows(query(table_selector), key_rename, columns))
    return columns, rows


def create_database_table(name, columns, rows):
    print('begin;')
    generate_table(name, columns)
    fill_table(name, columns, rows)
    print('commit;')


CREATE_TABLE = '''
create table {name} (
    id bigint primary key,
    {fields}
);
'''


def generate_table(name, columns):
    fields = generate_table_fields(columns)
    query = CREATE_TABLE.format(name=name, fields=',\n    '.join(fields))
    print(query)


INSERT = '''
insert into {name} (id, {fields})
values (%(id)s, {values});
'''

NONE_TYPE_VALUE = {int: 0, float: 0, str: ''}


def fill_table(name, columns, rows):
    query = INSERT.format(
        name=name,
        fields=', '.join(columns.keys()),
        values=', '.join(generate_query_values(columns)))
    for number, row in enumerate(rows):
        row['id'] = number
        for column_name, type_ in columns.items():
            if column_name not in row:
                row[column_name] = NONE_TYPE_VALUE[type_]
        print(query % {k: adapt(v) for k, v in row.items()})


def generate_rows(query, key_rename, columns):
    for tr in query('tr'):
        tr_query = PyQuery(tr)
        row = dict()
        for item in tr_query('td').items():
            key = item.attr('class')
            if key:
                key = key_rename(key)
                value = specialize(item.text())
                row[key] = value
                if key not in columns:
                    columns[key] = type(value)
                else:
                    columns[key] = general_type(columns[key], type(value))
        yield row


def int_with_comma(value):
    return int(value.replace(',', ''))


def int_with_space(value):
    return int(value.split(' ')[0])


def float_with_comma(value):
    return float(value.replace(',', ''))


def float_with_space(value):
    return float(value.split(' ')[0])


TYPES_CONSTRUCTORS = (
    int,
    int_with_comma,
    int_with_space,
    float,
    float_with_comma,
    float_with_space,
    str,
)


def specialize(value):
    for construct in TYPES_CONSTRUCTORS:
        try:
            return (construct(value.strip())
                    if value else NONE_TYPE_VALUE[construct])
        except ValueError:
            pass


PG_TYPES = {
    int: 'bigint',
    float: 'double precision',
    str: 'text',
}


def generate_table_fields(columns):
    for name, type_ in columns.items():
        yield '{name} {type}'.format(name=name, type=PG_TYPES[type_])


def generate_query_values(columns):
    for name in columns.keys():
        yield '%({name})s'.format(name=name)


TYPES_ORDER = {int: 0, float: 1, str: 2}


def general_type(a, b):
    return max(a, b, key=lambda v: TYPES_ORDER[v])
