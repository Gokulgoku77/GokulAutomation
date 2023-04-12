import time
import xmltodict
import pprint
import json
import pandas as pd
import numpy as np
import traceback
import re
import openpyxl
import xlsxwriter


def xml_to_dataframe(path):
    # Reading xml file and converting to dictionary
    with open(path, 'r', encoding='utf-8') as file:
        xml_data = file.read()
    xml_dict = xmltodict.parse(xml_data)

    # converting dictionary to json for viewing purpose
    xml_json = json.dumps(xml_dict)
    print(xml_json)
    sourceFile1 = open('demo1.json', 'w')
    print(xml_json, file=sourceFile1)
    sourceFile1.close()

    # Obtaining test cases
    xml_dict_tests = xml_dict['testReport']['components']['component']['testTool']['testRuns']['testRun']
    xml_dict_tests_cases_conditions = xml_dict_tests['test']

    # Creating empty dataframe for output
    df_data = pd.DataFrame()
    df_data['test_name'] = np.nan
    df_data['test_result'] = np.nan
    df_data['assertion_name'] = np.nan
    df_data['assertion_id'] = np.nan
    df_data['assertion_comment'] = np.nan
    df_data['assertion_result'] = np.nan
    df_data['comment'] = np.nan

    # For comparision and check
    lt = []
    dty = {'a': 'cg'}
    count = 0

    try:
        for test_data in xml_dict_tests_cases_conditions:
            print('*************************************************************************************')
            print('1st for')
            print(json.dumps(test_data))
            print(count)
            if test_data['conditions']:
                print('1st if')
                if type(test_data['conditions']['condition']) == type(lt):  # ?
                    print('2nd if')
                    for dt in test_data['conditions']['condition']:
                        print('2nd for')
                        print(json.dumps(dt))
                        print('here')
                        if dt['checks']:
                            print('3rd if')
                            if type(dt['checks']['check']) == type(dty):  # ?
                                print('z4th if')
                                print(json.dumps(dt))
                                print('out')
                                dict_check = {}
                                dict_check['assertion_name'] = dt['@conditionID']
                                dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                dict_check['test_result'] = test_data['score']['@value']
                                dict_check['assertion_id'] = dt['checks']['check']['@checkID']
                                # print(dt)
                                # print(dt['checks']['check']['score'])
                                # print(dict_check['assertion_name'])
                                dict_check['assertion_comment'] = dt['checks']['check']['comment']
                                dict_check['assertion_result'] = dt['checks']['check']['score']['@value']
                                if not dict_check['assertion_comment']:
                                    dict_check['assertion_comment'] = 'No comment'

                                df_check = pd.DataFrame(dict_check, index=[0])
                                df_check['assertion_comment'].replace(np.nan, 'No comment')
                                df_data = pd.concat([df_data, df_check], axis=0)
                            # elif type(dt['checks']['check']) == type(lt):
                            else:
                                print('Not a 4th if,it is else')
                                for check in dt['checks']['check']:
                                    dict_check = {}
                                    dict_check['assertion_name'] = dt['@conditionID']
                                    dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                    dict_check['test_result'] = test_data['score']['@value']
                                    dict_check['assertion_id'] = check['@checkID']
                                    dict_check['assertion_comment'] = check['comment']
                                    # print(dict_check['assertion_name'])
                                    if not dict_check['assertion_comment']:
                                        dict_check['assertion_comment'] = 'No comment'
                                    dict_check['assertion_result'] = check['score']['@value']
                                    df_check = pd.DataFrame(dict_check, index=[0])
                                    df_data = pd.concat([df_data, df_check], axis=0)
                        else:
                            print('Not a 3th if,it is else')
                            dict_check = {}
                            dict_check['assertion_name'] = dt['@conditionID']
                            dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                            dict_check['test_result'] = test_data['score']['@value']
                            dict_check['assertion_id'] = 'No Checks'
                            dict_check['assertion_comment'] = 'No Comment'
                            dict_check['assertion_result'] = dt['score']['@value']
                            df_check = pd.DataFrame(dict_check, index=[0])
                            df_data = pd.concat([df_data, df_check], axis=0)
                elif type(test_data['conditions']['condition']) == type(dty):
                    if test_data['conditions']['condition']:
                        new_dict = test_data['conditions']['condition']
                        print('thala', new_dict)
                        if new_dict['checks']:
                            checks = new_dict['checks']['check']
                            if type(checks) == type(dty):
                                print("FUNNY")
                                dict_check = {}
                                dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                                dict_check['test_result'] = test_data['score']['@value']
                                dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                dict_check['assertion_id'] = new_dict['checks']['check']['@checkID']
                                dict_check['assertion_comment'] = new_dict['checks']['check']['comment']
                                dict_check['assertion_result'] = new_dict['checks']['check']['score']['@value']
                                df_check = pd.DataFrame(dict_check, index=[0])
                                df_data = pd.concat([df_data, df_check], axis=0)
                            else:
                                if test_data['conditions']['condition'] and '@conditionID' in test_data['conditions']['condition']:
                                    print("day")
                                if test_data['conditions']['condition']['checks']:
                                    print("night")
                                    for check in test_data['conditions']['condition']['checks']['check']:
                                        dict_check = {}
                                        dict_check['assertion_name'] = test_data['conditions']['condition'][
                                            '@conditionID']
                                        dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                        dict_check['test_result'] = test_data['score']['@value']
                                        dict_check['assertion_id'] = check['@checkID']
                                        dict_check['assertion_comment'] = check['comment']
                                        # print(dict_check['assertion_name'])
                                        if not dict_check['assertion_comment']:
                                            dict_check['assertion_comment'] = 'No comment'
                                        dict_check['assertion_result'] = test_data['conditions']['condition']['score'][
                                            '@value']
                                        df_check = pd.DataFrame(dict_check, index=[0])
                                        df_check['assertion_comment'].replace(np.nan, 'No comment')
                                        df_data = pd.concat([df_data, df_check], axis=0)
                                else:
                                    print('mid night')
                                    dict_check = {}
                                    dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                                    dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                                    dict_check['test_result'] = test_data['score']['@value']
                                    dict_check['assertion_result'] = test_data['conditions']['condition']['score'][
                                        '@value']
                                    dict_check['assertion_id'] = 'No Checks'
                                    dict_check['assertion_comment'] = 'No comment'
                                    df_check = pd.DataFrame(dict_check, index=[0])
                                    df_check['assertion_comment'].replace(np.nan, 'No comment')
                                    df_data = pd.concat([df_data, df_check], axis=0)
                        else:
                            # for check in new_dict['checks']['check']:
                            dict_check = {}
                            dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                            dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                            dict_check['test_result'] = test_data['score']['@value']
                            df_check = pd.DataFrame(dict_check, index=[0])
                            df_data = pd.concat([df_data, df_check], axis=0)
                    else:
                        dict_check = {}
                        dict_check['assertion_name'] = test_data['conditions']['condition']['@conditionID']
                        dict_check['test_result'] = test_data['score']['@value']
                        dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                        dict_check['assertion_id'] = 'No_Checks'
                        dict_check['assertion_comment'] = 'No_Comments'
                        dict_check['assertion_result'] = 'n/a'
                        df_check = pd.DataFrame(dict_check, index=[0])
                        df_data = pd.concat([df_data, df_check], axis=0)
            else:
                print('No condition')
                dict_check = {}
                dict_check['test_name'] = test_data['@tcID'] + " " + test_data['title']
                dict_check['test_result'] = test_data['score']['@value']
                df_check = pd.DataFrame(dict_check, index=[0])
                df_data = pd.concat([df_data, df_check], axis=0)
            count = count + 1

    except Exception as e:
        # df_test = pd.DataFrame.from_dict(df_data)
        # print(df_test)
        # print(e)
        traceback.print_exc()
        return df_data.replace(np.nan, 'n/e')
        # .to_csv('chec.csv', index=False)
    df_data["assertion_id"].replace("", 'No-Checks', inplace=True)
    return df_data.replace(np.nan, 'No-Condition')


df_au = xml_to_dataframe('GRLReport_golden.xml')
df_gen = xml_to_dataframe('GRLReport.xml')

df_au.to_csv('golden.csv', index=False)
df_gen.to_csv('generated.csv', index=False)

df_au['check'] = df_au['test_name'] + df_au['assertion_name'] + df_au['assertion_id']
df_gen['check'] = df_gen['test_name'] + df_gen['assertion_name'] + df_gen['assertion_id']

gen_assertion_test_result = df_gen['test_result'].to_list()
gen_assertion_comment_list = df_gen['assertion_comment'].to_list()
gen_assertion_result_list = df_gen['assertion_result'].to_list()

gen_test_result_dict = {name: df_gen.iloc[df_gen['check'].to_list().index(name)]['test_result'] for name in
                        df_gen['check'].to_list()}
gen_assertion_result_dict = {name: df_gen.iloc[df_gen['check'].to_list().index(name)]['assertion_result'].strip() for
                             name in df_gen['check'].to_list()}
gen_assertion_comment_dict = {name: df_gen.iloc[df_gen['check'].to_list().index(name)]['assertion_comment'].strip() for
                              name in df_gen['check'].to_list()}
# print('zebra', gen_test_result_dict)

# test_name_list_au = df_au['test_name'].to_list()
# test_name_list_au1 = set(test_name_list_au)
# print('test_name_list_au',test_name_list_au1)
test_name_test_name_au = df_au['test_name'].drop_duplicates().to_list()
print('test_name_test_name_au', test_name_test_name_au)
test_name_test_name_gen = df_gen['test_name'].drop_duplicates().to_list()
print('test_name_test_name_gen',test_name_test_name_gen)
# for name in test_name_test_name_au:


# test_name_test_name_gen =df_gen['test_name'].drop_duplicates().to_list()
# print('test_name_test_name_gen',test_name_test_name_gen)

data_comp_dict = {
    'test_name': df_au['test_name'].to_list(),
    'golden_report_test_result': df_au['test_result'].to_list(),
    'generated_report_test_result': np.nan,
    'compared_result': '',
    'testCondition_name': df_au['assertion_name'].to_list(),
    'assertion_id': df_au['assertion_id'].to_list(),
    'golden_report_assertion_comment': df_au['assertion_comment'].to_list(),
    'generated_report_assertion_comment': np.nan,
    'golden_report_assertion_result': df_au['assertion_result'].to_list(),
    'generated_report_assertion_result': np.nan,
    'assertion_result': np.nan,
    'check': df_au['check'].to_list()
}

data_comp_dict1 = {
    'test_name': test_name_test_name_au,
}
# Creating empty dataframe for output
df_data_comp = pd.DataFrame(data_comp_dict)
df_data_comp1 = pd.DataFrame(data_comp_dict1)

test_list = df_data_comp['check'].to_list()
gen_test_list = df_gen['check'].to_list()
# print('test_list', test_list)
# print('gen_test_list', gen_test_list)

for name in test_list:
    # print(name)
    try:
        if name in gen_test_list:
            df_data_comp.at[test_list.index(name), 'generated_report_test_result'] = gen_test_result_dict[name]
            #print('qwert',gen_test_result_dict[name])
            df_data_comp.at[test_list.index(name), 'generated_report_assertion_result'] = gen_assertion_result_dict[
                name]
            df_data_comp.at[test_list.index(name), 'generated_report_assertion_comment'] = gen_assertion_comment_dict[
                name]
            df_data_comp.at[test_list.index(name), 'comment'] = 'Executed'
            # print('Zance', gen_test_result_dict[name])
    except Exception as e:
        pass
        print(e)

df_data_comp['compared_result'] = df_data_comp['golden_report_test_result'] == (
    df_data_comp['generated_report_test_result'])

df_data_comp['generated_report_assertion_result'].fillna('n/a', inplace=True)
df_data_comp['assertion_result'] = df_data_comp['golden_report_assertion_result'] == (
    df_data_comp['generated_report_assertion_result'])

df_data_comp.drop('check', axis=1, inplace=True)
# df_data_comp1.drop('golden_report_test_result', axis=1, inplace=True)
# df_data_comp1.drop('generated_report_test_result', axis=1, inplace=True)
# df_data_comp1.drop('compared_result', axis=1, inplace=True)
# df_data_comp['generated_report_assertion_result'].fillna('n/a', inplace=False)
# df_data_comp['compared_result'].fillna('NA', inplace=True)
# df_data_comp.fillna('no comment', inplace=True)
# df_data_comp.to_csv('outcheck.csv', index=False)

# def color_boolean(val):
#     return ['background-color: red' if x == False else 'background-color: green' for x in val]
#
#
# df_data_comp = df_data_comp.style.apply(color_boolean, axis=1, subset=['compared_result', 'assertion_result'])
# df_data_comp = df_data_comp.style.apply(color_boolean_na, axis=1, subset=['testCondition_name'])
# print(df_data_comp['generated_report_test_result'])
df_data_comp.to_excel('styled4.xlsx', engine='openpyxl', index=False)
#
# # ([‘test_name’, ‘compared_result’], as_index=false)
writer = pd.ExcelWriter('styled41.xlsx', engine='xlsxwriter')
#
# # Write the first DataFrame to a sheet named 'Sheet1'

#
# # Write the second DataFrame to a sheet named 'Sheet2'
df_data_comp["check"] = df_data_comp["golden_report_test_result"] + df_data_comp["test_name"]
print("ooo",df_data_comp["check"])
#B = df_data_comp['check'].drop_duplicates()
df_data_comp1["golden_report_test_result"] = df_data_comp['check'].drop_duplicates().to_list()
#B.to_csv('golden1.csv', index=False)

#for item in df_data_comp1["golden_report_test_result"].iteritems():
# df_data_comp["check"] = df_data_comp["generated_report_test_result"] + df_data_comp["test_name"]
# #df_data_comp1["generated_report_test_result"] = np.nan
# B = df_data_comp['check'].drop_duplicates()
# #df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates()
# B.to_csv('golden1.csv', index=False)
#if item in A:
#df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates()

# #df_data_comp["check"] = df_data_comp["generated_report_test_result"] + df_data_comp["test_name"]
# print("mmm",df_data_comp["check"])
# df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates()
# A= df_data_comp["check"].drop_duplicates()
# A.to_csv('golden2.csv', index=False)
print(len(df_data_comp['test_name'].drop_duplicates().to_list()))
dict_check = {}

for name in test_name_test_name_au:
    print('test name ', name)
    if name in test_name_test_name_gen:
        gip = df_data_comp[df_data_comp['test_name'] == name]['generated_report_test_result'].to_list()
        dict_check[name] = gip[0]
    else:
        dict_check[name] = 'n/a'

print(len(dict_check.values()))

del df_data_comp['golden_report_test_result']
del df_data_comp['generated_report_test_result']
del df_data_comp['compared_result']
del df_data_comp['check']
df_data_comp.to_excel(writer, sheet_name='Sheet1', index=False)
#df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates().to_list()

#df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates().to_list()
#print('cat',df_data_comp1["generated_report_test_result"])
# for name in test_name_test_name_au:
#     print('ban',name)
#     if name in test_name_test_name_gen:
#         print('gok',name)
#         df_data_comp["check"] = df_data_comp["generated_report_test_result"] + df_data_comp["test_name"]
#         df_data_comp1["generated_report_test_result"] = df_data_comp['check'].drop_duplicates().to_list()

def removeValue(string):
    #pattern = r'[*]'
    #string = re.sub(pattern, '', string)
    for x in string:
        if x == 'n':
            return string[:3]
        else:
            return string[:4]


df_data_comp1["golden_report_test_result"] = df_data_comp1["golden_report_test_result"].apply(removeValue)
df_data_comp1["generated_report_test_result"] = dict_check.values()

df_data_comp1.to_excel(writer, sheet_name='Sheet2', index=False)
writer.save()
# # Save the Excel
