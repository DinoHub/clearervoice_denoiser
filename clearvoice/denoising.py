from clearvoice import ClearVoice
import yaml

config = yaml.safe_load(open("/workdir/clearvoice/config.yaml"))

model_used = config['model']
noise_audio_dir = '/workdir/data/noisy'
clean_audio_dir = '/workdir/data/clean'

myClearVoice = ClearVoice(task='speech_enhancement', model_names=[model_used])
myClearVoice(input_path=noise_audio_dir, online_write=True, output_path=clean_audio_dir)