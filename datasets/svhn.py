from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import numpy as np
import h5py

from util import log

__PATH__ = './datasets/svhn'

rs = np.random.RandomState(123)


class Dataset(object):

    def __init__(self, ids, name='default',
                 max_examples=None, is_train=True):
        self._ids = list(ids)
        self.name = name
        self.is_train = is_train

        if max_examples is not None:
            self._ids = self._ids[:max_examples]

        filename = 'data.hdf5'

        file = os.path.join(__PATH__, filename)
        log.info("Reading %s ...", file)

        try:
            self.data = h5py.File(file, 'r')
        except:
            raise IOError('Dataset not found. Please make sure the dataset was downloaded.')
        log.info("Reading Done: %s", file)

    def get_data(self, id):
        # preprocessing and data augmentation
        m = self.data[id]['image'].value/255.
        l = self.data[id]['code'].value.astype(np.float32)

        # Data augmentation: rotate 0, 90, 180, 270
        """
        rot_num = np.floor(np.random.rand(1)*4)
        for i in range(rot_num):
            m = np.rot90(m, axes=(0, 1))
        m = m + np.random.randn(*m.shape) * 1e-2
        """
        return m, l

    @property
    def ids(self):
        return self._ids

    def __len__(self):
        return len(self.ids)

    def __repr__(self):
        return 'Dataset (%s, %d examples)' % (
            self.name,
            len(self)
        )


def get_data_info():
    return np.array([32, 32, 3, 25])


def get_conv_info():
    return np.array([64, 128, 256])


def get_deconv_info():
    return np.array([[384, 4, 2], [128, 4, 2], [64, 4, 2], [16, 4, 2], [3, 4, 2]])


def create_default_splits(is_train=True):
    ids = all_ids()

    num_trains = 73257

    dataset_train = Dataset(ids[:num_trains], name='train', is_train=False)
    dataset_test = Dataset(ids[num_trains:], name='test', is_train=False)
    return dataset_train, dataset_test


def all_ids():
    id_filename = 'id.txt'

    id_txt = os.path.join(__PATH__, id_filename)
    try:
        with open(id_txt, 'r') as fp:
            _ids = [s.strip() for s in fp.readlines() if s]
    except:
        raise IOError('Dataset not found. Please make sure the dataset was downloaded.')

    rs.shuffle(_ids)
    return _ids
