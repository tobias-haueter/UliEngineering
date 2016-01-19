#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities for generating chunks from datasets
"""
import numpy as np
import functools

def evaluateGeneratorFunction(tp, as_list=False):
    """
    Given a tuple (n, g) returned by one of the generator functions,
    evaluate the generator at all values.

    By default, returns a generator. Can also return a list if as_list=True
    """
    g, n = tp
    gen = (g(i) for i in range(n))
    return list(gen) if as_list else gen

def __fixedSizeChunkGeneratorWorker(ofsTable, chunksize, y, perform_copy, i):
    """Worker for fixedSizeChunkGenerator()"""
    yofs = ofsTable[i]
    yslice = y[yofs:yofs + chunksize]
    return yslice.copy() if perform_copy else yslice

def fixedSizeChunkGenerator(y, chunksize, shiftsize, perform_copy=True):
    """
    A chunk-generating function that can be used for parallelFFTSum().
    Generates only full chunks with variable chunk / shift size.

    If perform_copy=False, the chunk is not copied in the generator function.
    Functions like parallelFFTSum() modify the data which might lead to
    undesired overwriting of data. However, setting perform_copy=False might
    improve the performance significantly if the downstream function does
    not require copies.

    This is a lazy function, it generates copies only on-demand.

    Returns (g, n) where g is a unary generator function (which takes the chunk
        number as an argument) and n is the number of chunks.
    """
    # Precompute offset table
    offsets = [ofs for ofs in range(0, y.shape[0] - (chunksize - 1), shiftsize)]
    return functools.partial(__fixedSizeChunkGeneratorWorker, offsets, chunksize, y, perform_copy), len(offsets)

def reshapedChunks(arr, chunksize):
    """
    Generates virtual chunks of a numpy array by reshaping a view of the original array.
    Works really well with huge, mmapped arrays as no part of the array is copied.

    Automatically handles odd-sized arrays. Works only with 1D arrays.
    """
    if arr.shape[0] == 0:
        return arr
    # We might need to cut off some records for odd-shaped arrays
    end = arr.shape[0] - (arr.shape[0] % chunksize)
    v = arr[:end].view()
    v.shape = (-1, chunksize)
    return v
