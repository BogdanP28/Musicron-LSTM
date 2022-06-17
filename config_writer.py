from configparser import ConfigParser
config = ConfigParser()


config.read('config.ini')
config.add_section('PreprocessingParameters')

config.set('PreprocessingParameters', 'NR_TRAINING', '2')
config.set('PreprocessingParameters', 'COMPRESSION_FACTOR', '1')
config.set('PreprocessingParameters', 'CH_KEY', 'C')
config.set('PreprocessingParameters', 'NUMBER_OCTAVES', '1')
config.set('PreprocessingParameters', 'INSTRUMENT', 'Piano right')
config.set('PreprocessingParameters', 'INSTRUMENT_HARMONY', 'Piano left')
config.set('PreprocessingParameters', 'NUMERATOR', '4')
config.set('PreprocessingParameters', 'DENOMINATOR', '4')

with open('config.ini', 'w') as f:
    config.write(f)