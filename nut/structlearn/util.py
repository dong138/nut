#!/usr/bin/python
#
# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#
# License: BSD Style


"""
structlearn.util
================

"""
import operator
import functools
import numpy as np

from itertools import chain

def mask(instances, auxtask):
    """Sets all feature values for the features in
    auxtask to 0.
    
    Parameters
    ----------
    instances : array, shape = [n_instances], dtype=bolt.sparsedtype
        The instances whos features will be masked.
    auxtask : seq
        A sequence of features to be masked.

    Returns
    -------
    count : int
        The number of masked feature values.
    """
    count = 0
    for x in instances:
        indices = x['f0']
	for idx in auxtask:
	    if idx in indices:
		p = np.where(indices == idx)[0]
		if len(p) > 0:
		    x['f1'][p] = 0.0
		    count += 1
    return count

def autolabel(instances, auxtask):
    labels = np.ones((instances.shape[0],), dtype=np.float32)
    labels *= -1
    for i, x in enumerate(instances):
	indices = x['f0']
	for idx in auxtask:
	    if idx in indices:
		labels[i] = 1
		break
	
    return labels

def count(*datasets):
    """Counts the example frequency of each feature in a list
    of datasets. All data sets must have the same dimension.

    Returns
    -------
    counts : array, shape = [datasets[0].dim]
        counts[i] holds the number of examples in data sets for
        which the i-th feature is non-zero. 
    """
    if len(datasets) > 1:
	assert functools.reduce(operator.eq,[ds.dim for ds in datasets])
    counts = np.zeros((datasets[0].dim,),dtype=np.uint16)
    for x, y in chain(*datasets):
	counts[x["f0"]] += 1
    return counts
