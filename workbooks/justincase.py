# def get_counter_part(row):
#     if row['time'] == '6h':
#         v = tc[(tc['time'] == '05h') &
#            (tc['geno'] == row['geno']) &
#            (tc['treat'] == row['treat']) &
#            (tc['variable'] == row['variable'])]['value'].values
#     else:
#         v = tc[(tc['time'] == '6h') &
#            (tc['geno'] == row['geno']) &
#            (tc['treat'] == row['treat']) &
#            (tc['variable'] == row['variable'])]['value'].values

#     if v.size == 0:
#         return 0
#     else:
#         return float(v)
# tc['6h'] = tc.apply(get_counter_part, axis=1)
# tc.rename(columns={'value':'05h'}, inplace=True)
# tc = tc[tc['time'] == '05h'].drop(['sample','time'], axis=1)
