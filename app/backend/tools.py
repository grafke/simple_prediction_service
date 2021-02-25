import logging
import os

import pandas as pd

from app.backend.config import ALLOWED_EXTENSIONS
from app.backend.video_processor.video_processor import video_features

logger = logging.getLogger('app')


def allowed_file(filename):
    return allowed_extension(filename)


def allowed_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension in ALLOWED_EXTENSIONS


def prediction_probabilities(eval_features, trained_model, trained_features):
    query = pd.get_dummies(pd.DataFrame(eval_features))
    query = query.reindex(columns=trained_features, fill_value=0)
    fake_p, real_p = trained_model.predict_proba(query)[0]
    return {'p_fake': fake_p,
            'p_real': real_p}


def video_type_prediction(file_storage, trained_model, trained_features):
    file_abs_path = file_storage.saved_as()
    eval_features = video_features(file_abs_path)
    logger.info(eval_features)
    return prediction_probabilities(eval_features, trained_model, trained_features)
