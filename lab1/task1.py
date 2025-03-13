import subprocess
import csv
import chardet


def ping(host):
    return subprocess.run(['ping', '-n', '1', host], stdout=subprocess.PIPE)


def read(path):
    file=open(path)
    text=file.read()
    file.close()
    return text.splitlines()


def write(data, path):
    path=path+".csv"
    with open(path, mode='w', newline='') as csvfile:
        csvwriter=csv.writer(csvfile, delimiter=';')
        for row in data:
            csvwriter.writerow(row)


def parse_ping_output(output):
    lines=output.split('\rn')
    count=0
    stats=[]
    for word in lines[-1].split():
        count-=1
        if count==0:
            stats.append(word)
        if word in ["Максимальное", "Минимальное", "Среднее"]:
            count=2
    if stats:
        return stats
    else:
        return None


def main():
    input_file = 'sites.txt'
    output_file = 'ping_results'
    sites = read(input_file)
    results=[]
    for site in sites:
        print(f"Pinging {site}...")
        output = ping(site)
        output=output.stdout.decode('cp866')
        stats = parse_ping_output(output)
        if stats:
            results.append([site, stats[0][:-5], stats[1], stats[2]])
        else:
            print(f"Не удалось получить статистику для {site}")
    print(f"Результаты сохранены в {output_file}")


if __name__ == "__main__":
    main()
