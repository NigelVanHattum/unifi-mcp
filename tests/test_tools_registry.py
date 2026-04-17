"""Tests for tools registry — ALL_TOOLS completeness and dispatch routing."""

import pytest
from collections import Counter
import tools
from tools import (
    application, sites, devices, clients, networks,
    wifi, hotspot, firewall, acl, dns, traffic, supporting,
)


# ---------------------------------------------------------------------------
# Registry integrity
# ---------------------------------------------------------------------------

class TestRegistry:
    def test_total_tool_count(self):
        assert len(tools.ALL_TOOLS) == 62

    def test_no_duplicate_names(self):
        names = [t.name for t in tools.ALL_TOOLS]
        dupes = [n for n, c in Counter(names).items() if c > 1]
        assert dupes == [], f"Duplicate tool names: {dupes}"

    def test_all_tools_have_name_and_schema(self):
        for t in tools.ALL_TOOLS:
            assert t.name, "Tool missing name"
            assert t.inputSchema, f"Tool {t.name} missing inputSchema"

    def test_tool_names_sets_match_tools(self):
        """Each module's TOOL_NAMES must equal names in its TOOLS list."""
        for mod in [application, sites, devices, clients, networks,
                    wifi, hotspot, firewall, acl, dns, traffic, supporting]:
            declared = {t.name for t in mod.TOOLS}
            assert mod.TOOL_NAMES == declared, \
                f"{mod.__name__}: TOOL_NAMES mismatch"

    def test_dispatch_raises_for_unknown(self):
        with pytest.raises(ValueError, match="Unknown tool"):
            tools.dispatch("nonexistent_tool", {})

    @pytest.mark.parametrize("tool", tools.ALL_TOOLS)
    def test_required_fields_are_in_properties(self, tool):
        """Every required field must appear in properties."""
        schema = tool.inputSchema
        required = schema.get("required", [])
        props = schema.get("properties", {})
        missing = [f for f in required if f not in props]
        assert not missing, \
            f"{tool.name}: required fields not in properties: {missing}"


# ---------------------------------------------------------------------------
# Module tool counts
# ---------------------------------------------------------------------------

class TestModuleCounts:
    def test_application(self):  assert len(application.TOOLS) == 1
    def test_sites(self):        assert len(sites.TOOLS) == 1
    def test_devices(self):      assert len(devices.TOOLS) == 8
    def test_clients(self):      assert len(clients.TOOLS) == 3
    def test_networks(self):     assert len(networks.TOOLS) == 6
    def test_wifi(self):         assert len(wifi.TOOLS) == 5
    def test_hotspot(self):      assert len(hotspot.TOOLS) == 5
    def test_firewall(self):     assert len(firewall.TOOLS) == 13
    def test_acl(self):          assert len(acl.TOOLS) == 7
    def test_dns(self):          assert len(dns.TOOLS) == 5
    def test_traffic(self):      assert len(traffic.TOOLS) == 5
    def test_supporting(self):   assert len(supporting.TOOLS) == 3
