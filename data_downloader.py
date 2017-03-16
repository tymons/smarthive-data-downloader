import requests
import json
import csv
import collections

def get_token( username, password ):
    payload = {'username': username, 'password': password}
    r = requests.post('http://raspeul.hopto.org:8080/smarthive/user/auth', json=payload)
    return json.loads(r.text)['token']

def get_available_sounds( token, hive_id ):
    payload = {'from' : '2010-01-11T12:12:10', 'to' : '2020-11-12T23:13:10'}
    headers = {'token': token}
    r = requests.get('http://raspeul.hopto.org:8080/smarthive/measurement/sound/' + str(hive_id) + '/getAvailableSounds', headers=headers, params=payload)
    json_obj = json.loads(r.text)
    return list(json_obj.values())

def read_last_download_id():
    f = open('last_id.txt', 'r')
    idx = f.read()
    f.close()
    return idx;

def write_last_download_id( idx ):
    f = open('last_id.txt', 'r+')
    f.truncate()
    f.write(str(idx))
    f.close()

def create_csv_file( probes, file_name ):
    writer = csv.writer(open('csvresults/' + file_name + '-soundvalues.csv', 'w', newline=''),
                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['probe value'])
    for probe in probes:
        writer.writerow([int(probe)])

def get_probes_create_charts( token, hive_id, sounds_idx, start_idx ):
    last_idx = start_idx;
    sounds_idx_sorted = sorted(sounds_idx)
    for sound_idx in sounds_idx_sorted:
        if (start_idx < sound_idx):
            payload = {'soundId' : sound_idx}
            headers = {'token': token}
            r = requests.get('http://raspeul.hopto.org:8080/smarthive/measurement/sound/' + str(hive_id), headers=headers, params=payload)
            probesMic1 = json.loads(r.text)['valuesMic1']
            create_csv_file(probesMic1, 'mic1/' + str(sound_idx) + '-' + json.loads(r.text)['timestamp'])
            probesMic2 = json.loads(r.text)['valuesMic2']
            create_csv_file(probesMic2, 'mic2/' + str(sound_idx) + '-' + json.loads(r.text)['timestamp'])
            probesMic3 = json.loads(r.text)['valuesMic3']
            create_csv_file(probesMic3, 'mic3/' + str(sound_idx) + '-' + json.loads(r.text)['timestamp'])
            probesMic4 = json.loads(r.text)['valuesMic4']
            create_csv_file(probesMic4, 'mic4/' + str(sound_idx) + '-' + json.loads(r.text)['timestamp'])
            last_idx = sound_idx;

    return last_idx;

def main():
    #Get token for Authorization
    token = get_token( 'tymons', '43210')

    #Get ids of all avaliable sounds for hive with specific id
    sounds_map = get_available_sounds( token, 2 )
    #Read where you finished last time
    start_idx = read_last_download_id();

    last_idx = get_probes_create_charts(token, 2, sounds_map, int(start_idx) )
    #Create
    write_last_download_id(str(last_idx))


if __name__ == "__main__":
    main()
