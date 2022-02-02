#!/usr/bin/env python3
"""
Utilities for iterables
"""
import collections
import collections.abc

__all__ = ["PeekableIteratorWrapper", "ListIterator", "skip_first"]

class ListIterator(object):
    """
    Takes an iterable (like a list)
    and exposes a generator-like interface.

    The given iterable must support len()
    and index-based access
    for this algorithm to work.

    Equivalent to (v for v in lst)
    except calling len() reveals
    how many values are left to iterate.

    Use .index to access the current index.
    """
    def __init__(self, lst):
        self.index = 0
        self._lst = lst
        self._remaining = len(self._lst)

    def __iter__(self):
        return self

    def __next__(self):
        if self._remaining <= 0:
            raise StopIteration
        v = self._lst[self.index]
        self.index += 1
        self._remaining -= 1
        return v

    def __len__(self):
        """Remaining values"""
        return self._remaining

    


def iterable_to_iterator(it):
    """
    Given an iterable (like a list), generates
    an iterable out
    """

class PeekableIteratorWrapper(object):
    """
    Wraps an iterator and provides the additional
    capability of 'peeking' and un-getting values.

    Works by storing un-got values in a buffer
    that is emptied on call to next() before
    touching the child iterator.

    The buffer is managed in a stack-like manner
    (LIFO) so you can un-get multiple values.
    """
    def __init__(self, child):
        """
        Initialize a PeekableIteratorWrapper
        with a given child iterator
        """
        self.buffer = []
        self.child = child

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.buffer) > 0:
            return self.buffer.pop()
        return next(self.child)
    
    def __len__(self):
        """
        Returns len(child). Only supported
        if child support len().
        """
        return len(self.child)

    def has_next(self):
        """
        Returns False only if the next call to next()
        will raise StopIteration.

        This causes the next value to be generated from
        the child generator (and un-got) if there are no
        values in the buffer
        """
        if len(self.buffer) > 0:
            return True
        else:
            try:
                v = next(self)
                self.unget(v)
                return True
            except StopIteration:
                return False
            

    def unget(self, v):
        """
        Un-gets v so that v will be returned
        on the next call to __next__ (unless
        another value is un-got after this).
        """
        self.buffer.append(v)

    def peek(self):
        """
        Get the next value without removing it from
        the iterator.

        Note: Multiple subsequent calls to peek()
        without any calls to __next__() in between
        will return the same value.
        """
        val = next(self)
        self.unget(val)
        return val

def skip_first(it):
    """
    Skip the first element of an Iterator or Iterable,
    like a Generator or a list.

    This will always return a generator or raise TypeError()
    in case the argument's type is not compatible
    """
    if isinstance(it, collections.abc.Iterator):
        try:
            next(it)
            yield from it
        except StopIteration:
            return
    elif isinstance(it, collections.abc.Iterable):
        yield from skip_first(it.__iter__())
    else:
        raise TypeError(f"You must pass an Iterator or an Iterable to skip_first(), but you passed {it}")

