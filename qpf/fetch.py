from ftplib import FTP
import os
import tarfile

TAR_FOLDER = os.path.join('..', 'tar')
SHP_FOLDER = os.path.join('..', 'shp')

# (period, duration, start): (folder, filename)
QPF_FILES = {
    ('day1', 24, 0): ('day1', 'QPF24hr_Day1_latest'),
    ('day1', 6, 0): ('day1', 'QPF6hr_f00-f06_latest'),
    ('day1', 6, 6): ('day1', 'QPF6hr_f06-f12_latest'),
    ('day1', 6, 12): ('day1', 'QPF6hr_f12-f18_latest'),
    ('day1', 6, 18): ('day1', 'QPF6hr_f18-f24_latest'),
    ('day1', 6, 24): ('day1', 'QPF6hr_f24-f30_latest'),
    ('day2', 24, 0): ('day2', 'QPF24hr_Day2_latest'),
    ('day2', 6, 30): ('day2', 'QPF6hr_f30-f36_latest'),
    ('day2', 6, 36): ('day2', 'QPF6hr_f36-f42_latest'),
    ('day2', 6, 42): ('day2', 'QPF6hr_f42-f48_latest'),
    ('day2', 6, 48): ('day2', 'QPF6hr_f48-f54_latest'),
    ('day3', 24, 0): ('day3', 'QPF24hr_Day3_latest'),
    ('day3', 6, 54): ('day3', 'QPF6hr_f54-f60_latest'),
    ('day3', 6, 60): ('day3', 'QPF6hr_f60-f66_latest'),
    ('day3', 6, 66): ('day3', 'QPF6hr_f66-f72_latest'),
    ('day3', 6, 72): ('day3', 'QPF6hr_f72-f78_latest'),
    ('day45', 48, 0): ('day45', 'QPF48hr_Day4-5_latest'),
    ('day67', 48, 0): ('day67', 'QPF48hr_Day6-7_latest'),
    ('5day', 120, 0): ('5day', 'QPF120hr_Day1-5_latest'),
    # ('7day', 120, 0): ('7day', 'QPF120hr_Day1-5_latest'),
    ('7day', 168, 0): ('7day', 'QPF168hr_Day1-7_latest')
}


def fetch_tar(period, duration, start, output_folder=TAR_FOLDER):
    """Download QPF tar file containing shapefile and save to output_folder"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        folder, filename = QPF_FILES[(period, duration, start)]
    except KeyError:
        message = 'Invalid combination of period, duration, and start: %s, %d, %d' % (period, duration, start)
        raise KeyError(message)
    filename = filename + '.tar'
    output_path = os.path.join(output_folder, folder, filename)
    if not os.path.exists(os.path.join(output_folder, folder)):
        os.makedirs(os.path.join(output_folder, folder))
    ftp = FTP('ftp.hpc.ncep.noaa.gov')
    ftp.login(user='anonymous', passwd='walker.jeff.d@gmail.com')
    ftp.cwd('/shapefiles/qpf/' + folder)
    with open(output_path, 'wb') as out:
        try:
            ftp.retrbinary('RETR ' + filename, out.write)
        except:
            print 'ERROR: could not fetch file %s' % os.path.join(folder, filename)
    ftp.close()
    return folder, filename

def extract_tar(folder, filename, input_folder=TAR_FOLDER, output_folder=SHP_FOLDER):
    """Extract QPF tar file"""
    if not os.path.exists(os.path.join(output_folder, folder)):
        os.makedirs(os.path.join(output_folder, folder))

    filepath = os.path.join(folder, filename)
    t = tarfile.open(os.path.join(input_folder, filepath))
    tar_filenames = [m.name for m in t.getmembers()]
    shp_filename = [name for name in tar_filenames if name.endswith('.shp')][0]

    file_folder = os.path.dirname(filepath)
    output_path = os.path.join(output_folder, file_folder)
    t.extractall(output_path)

    return output_path, shp_filename

def fetch_and_extract(period, duration, start, tar_folder=TAR_FOLDER, shp_folder=SHP_FOLDER):
    folder, filename = fetch_tar(period, duration, start, output_folder=tar_folder)
    folder, filename = extract_tar(folder, filename, input_folder=tar_folder, output_folder=shp_folder)
    return folder, filename

if __name__ == '__main__':
    print fetch_and_extract('day1', 6, 0)