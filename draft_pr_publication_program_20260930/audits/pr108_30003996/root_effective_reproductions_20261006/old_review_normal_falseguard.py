def require(value, message='verification predicate failed'):
 if not value: raise AssertionError(message)
require(False, "intentional known-false control")
