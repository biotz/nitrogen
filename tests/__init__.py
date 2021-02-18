import pytest

SKIP_INTEGRATION = False
SKIP_E2E = True

integration = pytest.mark.skipif(SKIP_INTEGRATION, reason="INTEGRATION TEST SKIP")
e2e = pytest.mark.skipif(SKIP_E2E, reason="END TO END TEST SKIP")
