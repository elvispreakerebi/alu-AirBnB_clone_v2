from collections.abc import Mapping
import operator
operator.isMappingType = lambda obj: isinstance(obj, Mapping)
