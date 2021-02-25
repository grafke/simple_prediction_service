import numpy as np
import os

from moviepy.editor import VideoFileClip
import ffmpeg
from scipy import stats


def video_features(filename):
    result = {'duration': [],
              'aspect_ratio': [],
              'fps': [],
              'audio_duration': [],
              'vol_std': [],
              'vol_mean': [],
              'vol_mode': [],
              'fsize': [],
              'w': [],
              'h': [],
              'profile_0_Constrained_Baseline': [],
              'profile_0_High': [],
              'profile_0_Main': [],
              'profile_1_HE-AAC': [],
              'profile_1_HE-AACv2': [],
              'profile_1_LC': [],
              'mono_eq_stereo': [],
              'mono_stereo_diff_std': [],
              'mono_stereo_diff_mean': [],
              'mono_stereo_diff_mode': []
              }
    result['fsize'].append(os.path.getsize(filename) / 1024 / 1024)

    video = VideoFileClip(filename)
    result['duration'].append(video.duration)
    result['aspect_ratio'].append(video.aspect_ratio)
    result['fps'].append(video.fps)
    result['w'] = video.size[0]
    result['h'] = video.size[1]

    audio = video.audio
    result['audio_duration'].append(audio.duration if audio else -1)

    mono, stereo = mono_stereo(audio, video)
    mono_stereo_diff = [i[0] - i[1] for i in zip(mono, stereo)]
    result['mono_stereo_diff_std'] = np.std(mono_stereo_diff)
    result['mono_stereo_diff_mean'] = np.mean(mono_stereo_diff)
    result['mono_stereo_diff_mode'] = stats.mode(mono_stereo_diff)[0][0]
    result['mono_eq_stereo'] = 1 if mono == stereo else 0

    volumes = sound_volumes(audio, video)
    result['vol_std'] = np.std(volumes)
    result['vol_mean'] = np.mean(volumes)
    result['vol_mode'] = stats.mode(volumes)[0][0]

    probe = ffmpeg.probe(filename)
    profile_0 = probe.get('streams')[0].get('profile')
    profile_1 = probe.get('streams')[1].get('profile') if len(probe.get('streams')) > 1 else None

    result['profile_0_Constrained_Baseline'] = 1 if profile_0 == 'Constrained Baseline' else 0
    result['profile_0_High'] = 1 if profile_0 == 'High' else 0
    result['profile_0_Main'] = 1 if profile_0 == 'Main' else 0
    result['profile_1_HE-AAC'] = 1 if profile_1 == 'HE-AAC' else 0
    result['profile_1_HE-AACv2'] = 1 if profile_1 == 'HE-AACv2' else 0
    result['profile_1_LC'] = 1 if profile_1 == 'LC' else 0

    return result


def mono_stereo(audio, video):
    duration = video.duration
    step = 0.1
    audio_frames = []
    for t in range(int(duration / step)):
        t = t * step
        if t > audio.duration or t > video.duration: break
        audio_frames.append(audio.get_frame(t))  # numpy array representing mono/stereo values
    mono = [i[0] for i in audio_frames]
    stereo = [i[1] for i in audio_frames]
    return mono, stereo


def sound_volumes(audio, video):
    cut = lambda i: video.audio.subclip(i, i + 1).to_soundarray(fps=22000)
    volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())

    if audio:
        volumes = [volume(cut(i)) for i in range(0, int(video.audio.duration - 2))]
    else:
        volumes = [-1 for i in range(0, int(video.duration - 2))]

    return volumes
