"""Tests for dispatch() in every tool module — verifies correct HTTP method/path/body/params."""

import pytest
from unittest.mock import patch, MagicMock, call


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_api_mock(return_value=None):
    """Patch client.api and return the mock."""
    m = MagicMock(return_value=return_value or {"status": "success"})
    return m


def run(module, name, args, api_mock):
    """Call module.dispatch with api patched."""
    target = f"{module.__name__}.api"
    with patch(target, api_mock):
        return module.dispatch(name, args)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

from tools import application

class TestApplicationDispatch:
    def test_get_application_info(self):
        m = make_api_mock({"version": "7.0"})
        run(application, "get_application_info", {}, m)
        m.assert_called_once_with("GET", "/info")


# ---------------------------------------------------------------------------
# Sites
# ---------------------------------------------------------------------------

from tools import sites

class TestSitesDispatch:
    def test_list_sites_no_params(self):
        m = make_api_mock()
        run(sites, "list_sites", {}, m)
        m.assert_called_once_with("GET", "/sites", params={})

    def test_list_sites_with_params(self):
        m = make_api_mock()
        run(sites, "list_sites", {"limit": 10, "offset": 0}, m)
        m.assert_called_once_with("GET", "/sites", params={"limit": 10, "offset": 0})


# ---------------------------------------------------------------------------
# Devices
# ---------------------------------------------------------------------------

from tools import devices

class TestDevicesDispatch:
    def test_list_adopted_devices(self):
        m = make_api_mock()
        run(devices, "list_adopted_devices", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/devices", params={})

    def test_list_adopted_devices_with_filter(self):
        m = make_api_mock()
        run(devices, "list_adopted_devices", {"siteId": "s1", "limit": 5}, m)
        m.assert_called_once_with("GET", "/sites/s1/devices", params={"limit": 5})

    def test_adopt_device(self):
        m = make_api_mock()
        run(devices, "adopt_device",
            {"siteId": "s1", "macAddress": "aa:bb:cc:dd:ee:ff", "ignoreDeviceLimit": False}, m)
        m.assert_called_once_with("POST", "/sites/s1/devices",
                                  body={"macAddress": "aa:bb:cc:dd:ee:ff",
                                        "ignoreDeviceLimit": False})

    def test_get_adopted_device(self):
        m = make_api_mock()
        run(devices, "get_adopted_device", {"siteId": "s1", "deviceId": "d1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/devices/d1")

    def test_remove_device(self):
        m = make_api_mock()
        run(devices, "remove_device", {"siteId": "s1", "deviceId": "d1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/devices/d1")

    def test_get_device_statistics(self):
        m = make_api_mock()
        run(devices, "get_device_statistics", {"siteId": "s1", "deviceId": "d1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/devices/d1/statistics/latest")

    def test_execute_device_action(self):
        m = make_api_mock()
        run(devices, "execute_device_action",
            {"siteId": "s1", "deviceId": "d1", "action": "RESTART"}, m)
        m.assert_called_once_with("POST", "/sites/s1/devices/d1/actions",
                                  body={"action": "RESTART"})

    def test_execute_port_action(self):
        m = make_api_mock()
        run(devices, "execute_port_action",
            {"siteId": "s1", "deviceId": "d1", "portIdx": 3, "action": "POWER_CYCLE"}, m)
        m.assert_called_once_with(
            "POST",
            "/sites/s1/devices/d1/interfaces/ports/3/actions",
            body={"action": "POWER_CYCLE"},
        )

    def test_list_pending_devices(self):
        m = make_api_mock()
        run(devices, "list_pending_devices", {}, m)
        m.assert_called_once_with("GET", "/pending-devices", params={})


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------

from tools import clients

class TestClientsDispatch:
    def test_list_clients(self):
        m = make_api_mock()
        run(clients, "list_clients", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/clients", params={})

    def test_get_client(self):
        m = make_api_mock()
        run(clients, "get_client", {"siteId": "s1", "clientId": "c1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/clients/c1")

    def test_execute_client_action_authorize(self):
        m = make_api_mock()
        run(clients, "execute_client_action",
            {"siteId": "s1", "clientId": "c1", "action": "AUTHORIZE_GUEST_ACCESS",
             "timeLimitMinutes": 60}, m)
        m.assert_called_once_with(
            "POST", "/sites/s1/clients/c1/actions",
            body={"action": "AUTHORIZE_GUEST_ACCESS", "timeLimitMinutes": 60},
        )

    def test_execute_client_action_unauthorize(self):
        m = make_api_mock()
        run(clients, "execute_client_action",
            {"siteId": "s1", "clientId": "c1", "action": "UNAUTHORIZE_GUEST_ACCESS"}, m)
        m.assert_called_once_with(
            "POST", "/sites/s1/clients/c1/actions",
            body={"action": "UNAUTHORIZE_GUEST_ACCESS"},
        )


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------

from tools import networks

class TestNetworksDispatch:
    def test_list_networks(self):
        m = make_api_mock()
        run(networks, "list_networks", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/networks", params={})

    def test_create_network(self):
        m = make_api_mock()
        args = {"siteId": "s1", "management": "GATEWAY", "name": "IoT",
                "enabled": True, "vlanId": 20}
        run(networks, "create_network", args, m)
        m.assert_called_once_with("POST", "/sites/s1/networks",
                                  body={"management": "GATEWAY", "name": "IoT",
                                        "enabled": True, "vlanId": 20})

    def test_get_network(self):
        m = make_api_mock()
        run(networks, "get_network", {"siteId": "s1", "networkId": "n1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/networks/n1")

    def test_update_network(self):
        m = make_api_mock()
        args = {"siteId": "s1", "networkId": "n1", "management": "SWITCH",
                "name": "Corp", "enabled": True, "vlanId": 10}
        run(networks, "update_network", args, m)
        m.assert_called_once_with("PUT", "/sites/s1/networks/n1",
                                  body={"management": "SWITCH", "name": "Corp",
                                        "enabled": True, "vlanId": 10})

    def test_delete_network_no_force(self):
        m = make_api_mock()
        run(networks, "delete_network", {"siteId": "s1", "networkId": "n1"}, m)
        # force=None → stripped by omit inside api(), passed as {"force": None}
        m.assert_called_once_with("DELETE", "/sites/s1/networks/n1",
                                  params={"force": None})

    def test_delete_network_force(self):
        m = make_api_mock()
        run(networks, "delete_network", {"siteId": "s1", "networkId": "n1", "force": True}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/networks/n1",
                                  params={"force": True})

    def test_get_network_references(self):
        m = make_api_mock()
        run(networks, "get_network_references", {"siteId": "s1", "networkId": "n1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/networks/n1/references")


# ---------------------------------------------------------------------------
# WiFi
# ---------------------------------------------------------------------------

from tools import wifi

class TestWifiDispatch:
    def test_list_wifi_broadcasts(self):
        m = make_api_mock()
        run(wifi, "list_wifi_broadcasts", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/wifi/broadcasts", params={})

    def test_create_wifi_broadcast(self):
        m = make_api_mock()
        args = {"siteId": "s1", "type": "STANDARD", "name": "MyNet",
                "enabled": True, "securityConfiguration": {"type": "WPA2"},
                "multicastToUnicastConversionEnabled": False,
                "clientIsolationEnabled": False, "hideName": False, "uapsdEnabled": True}
        run(wifi, "create_wifi_broadcast", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert body["name"] == "MyNet"

    def test_get_wifi_broadcast(self):
        m = make_api_mock()
        run(wifi, "get_wifi_broadcast",
            {"siteId": "s1", "wifiBroadcastId": "wb1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/wifi/broadcasts/wb1")

    def test_update_wifi_broadcast(self):
        m = make_api_mock()
        args = {"siteId": "s1", "wifiBroadcastId": "wb1", "type": "STANDARD",
                "name": "Updated", "enabled": True,
                "securityConfiguration": {}, "multicastToUnicastConversionEnabled": False,
                "clientIsolationEnabled": False, "hideName": False, "uapsdEnabled": False}
        run(wifi, "update_wifi_broadcast", args, m)
        _, kwargs = m.call_args
        assert m.call_args.args == ("PUT", "/sites/s1/wifi/broadcasts/wb1")
        assert kwargs["body"] == {"type": "STANDARD", "name": "Updated",
                                  "enabled": True, "securityConfiguration": {},
                                  "multicastToUnicastConversionEnabled": False,
                                  "clientIsolationEnabled": False,
                                  "hideName": False, "uapsdEnabled": False}

    def test_delete_wifi_broadcast(self):
        m = make_api_mock()
        run(wifi, "delete_wifi_broadcast",
            {"siteId": "s1", "wifiBroadcastId": "wb1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/wifi/broadcasts/wb1",
                                  params={"force": None})


# ---------------------------------------------------------------------------
# Hotspot
# ---------------------------------------------------------------------------

from tools import hotspot

class TestHotspotDispatch:
    def test_list_vouchers(self):
        m = make_api_mock()
        run(hotspot, "list_vouchers", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/hotspot/vouchers", params={})

    def test_create_vouchers(self):
        m = make_api_mock()
        args = {"siteId": "s1", "name": "guest", "timeLimitMinutes": 120, "count": 5}
        run(hotspot, "create_vouchers", args, m)
        m.assert_called_once_with("POST", "/sites/s1/hotspot/vouchers",
                                  body={"name": "guest", "timeLimitMinutes": 120, "count": 5})

    def test_delete_vouchers_by_filter(self):
        m = make_api_mock()
        run(hotspot, "delete_vouchers",
            {"siteId": "s1", "filter": "name=='guest'"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/hotspot/vouchers",
                                  params={"filter": "name=='guest'"})

    def test_get_voucher(self):
        m = make_api_mock()
        run(hotspot, "get_voucher", {"siteId": "s1", "voucherId": "v1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/hotspot/vouchers/v1")

    def test_delete_voucher(self):
        m = make_api_mock()
        run(hotspot, "delete_voucher", {"siteId": "s1", "voucherId": "v1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/hotspot/vouchers/v1")


# ---------------------------------------------------------------------------
# Firewall
# ---------------------------------------------------------------------------

from tools import firewall

class TestFirewallDispatch:
    def test_list_firewall_zones(self):
        m = make_api_mock()
        run(firewall, "list_firewall_zones", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/firewall/zones", params={})

    def test_get_firewall_zone(self):
        m = make_api_mock()
        run(firewall, "get_firewall_zone",
            {"siteId": "s1", "firewallZoneId": "z1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/firewall/zones/z1")

    def test_create_firewall_zone(self):
        m = make_api_mock()
        run(firewall, "create_firewall_zone",
            {"siteId": "s1", "name": "DMZ", "networkIds": ["n1", "n2"]}, m)
        m.assert_called_once_with("POST", "/sites/s1/firewall/zones",
                                  body={"name": "DMZ", "networkIds": ["n1", "n2"]})

    def test_update_firewall_zone(self):
        m = make_api_mock()
        run(firewall, "update_firewall_zone",
            {"siteId": "s1", "firewallZoneId": "z1", "name": "LAN", "networkIds": ["n3"]}, m)
        m.assert_called_once_with("PUT", "/sites/s1/firewall/zones/z1",
                                  body={"name": "LAN", "networkIds": ["n3"]})

    def test_delete_firewall_zone(self):
        m = make_api_mock()
        run(firewall, "delete_firewall_zone",
            {"siteId": "s1", "firewallZoneId": "z1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/firewall/zones/z1")

    def test_list_firewall_policies(self):
        m = make_api_mock()
        run(firewall, "list_firewall_policies", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/firewall/policies", params={})

    def test_get_firewall_policy(self):
        m = make_api_mock()
        run(firewall, "get_firewall_policy",
            {"siteId": "s1", "firewallPolicyId": "p1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/firewall/policies/p1")

    def test_create_firewall_policy(self):
        m = make_api_mock()
        args = {"siteId": "s1", "enabled": True, "name": "Block WAN",
                "action": {"type": "BLOCK"},
                "source": {"zoneId": "z1"}, "destination": {"zoneId": "z2"},
                "ipProtocolScope": {"ipVersion": "IPV4"},
                "loggingEnabled": False}
        run(firewall, "create_firewall_policy", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert body["name"] == "Block WAN"

    def test_update_firewall_policy(self):
        m = make_api_mock()
        args = {"siteId": "s1", "firewallPolicyId": "p1", "enabled": True,
                "name": "Allow LAN", "action": {"type": "ALLOW"},
                "source": {"zoneId": "z1"}, "destination": {"zoneId": "z2"},
                "ipProtocolScope": {}, "loggingEnabled": True}
        run(firewall, "update_firewall_policy", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert "firewallPolicyId" not in body

    def test_delete_firewall_policy(self):
        m = make_api_mock()
        run(firewall, "delete_firewall_policy",
            {"siteId": "s1", "firewallPolicyId": "p1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/firewall/policies/p1")

    def test_patch_firewall_policy(self):
        m = make_api_mock()
        run(firewall, "patch_firewall_policy",
            {"siteId": "s1", "firewallPolicyId": "p1", "loggingEnabled": True}, m)
        m.assert_called_once_with("PATCH", "/sites/s1/firewall/policies/p1",
                                  body={"loggingEnabled": True})

    def test_get_firewall_policy_ordering(self):
        m = make_api_mock()
        run(firewall, "get_firewall_policy_ordering",
            {"siteId": "s1", "sourceFirewallZoneId": "z1", "destinationFirewallZoneId": "z2"}, m)
        m.assert_called_once_with(
            "GET", "/sites/s1/firewall/policies/ordering",
            params={"sourceFirewallZoneId": "z1", "destinationFirewallZoneId": "z2"},
        )

    def test_update_firewall_policy_ordering(self):
        m = make_api_mock()
        ordered = {"beforeSystemDefined": ["p1", "p2"], "afterSystemDefined": []}
        run(firewall, "update_firewall_policy_ordering",
            {"siteId": "s1", "sourceFirewallZoneId": "z1",
             "destinationFirewallZoneId": "z2",
             "orderedFirewallPolicyIds": ordered}, m)
        m.assert_called_once_with(
            "PUT", "/sites/s1/firewall/policies/ordering",
            params={"sourceFirewallZoneId": "z1", "destinationFirewallZoneId": "z2"},
            body={"orderedFirewallPolicyIds": ordered},
        )


# ---------------------------------------------------------------------------
# ACL
# ---------------------------------------------------------------------------

from tools import acl

class TestAclDispatch:
    def test_list_acl_rules(self):
        m = make_api_mock()
        run(acl, "list_acl_rules", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/acl-rules", params={})

    def test_get_acl_rule(self):
        m = make_api_mock()
        run(acl, "get_acl_rule", {"siteId": "s1", "aclRuleId": "r1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/acl-rules/r1")

    def test_create_acl_rule(self):
        m = make_api_mock()
        args = {"siteId": "s1", "type": "IPV4", "enabled": True,
                "name": "Block Telnet", "action": "BLOCK"}
        run(acl, "create_acl_rule", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert body["action"] == "BLOCK"

    def test_update_acl_rule(self):
        m = make_api_mock()
        args = {"siteId": "s1", "aclRuleId": "r1", "type": "IPV4",
                "enabled": False, "name": "Renamed", "action": "ALLOW"}
        run(acl, "update_acl_rule", args, m)
        m.assert_called_once_with("PUT", "/sites/s1/acl-rules/r1",
                                  body={"type": "IPV4", "enabled": False,
                                        "name": "Renamed", "action": "ALLOW"})

    def test_delete_acl_rule(self):
        m = make_api_mock()
        run(acl, "delete_acl_rule", {"siteId": "s1", "aclRuleId": "r1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/acl-rules/r1")

    def test_get_acl_rule_ordering(self):
        m = make_api_mock()
        run(acl, "get_acl_rule_ordering", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/acl-rules/ordering")

    def test_update_acl_rule_ordering(self):
        m = make_api_mock()
        run(acl, "update_acl_rule_ordering",
            {"siteId": "s1", "orderedAclRuleIds": ["r2", "r1"]}, m)
        m.assert_called_once_with("PUT", "/sites/s1/acl-rules/ordering",
                                  body={"orderedAclRuleIds": ["r2", "r1"]})


# ---------------------------------------------------------------------------
# DNS
# ---------------------------------------------------------------------------

from tools import dns

class TestDnsDispatch:
    def test_list_dns_policies(self):
        m = make_api_mock()
        run(dns, "list_dns_policies", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/dns/policies", params={})

    def test_get_dns_policy(self):
        m = make_api_mock()
        run(dns, "get_dns_policy", {"siteId": "s1", "dnsPolicyId": "dp1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/dns/policies/dp1")

    def test_create_dns_policy(self):
        m = make_api_mock()
        args = {"siteId": "s1", "type": "A_RECORD", "enabled": True,
                "domain": "local.example.com", "ipv4Address": "192.168.1.50"}
        run(dns, "create_dns_policy", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert body["domain"] == "local.example.com"

    def test_update_dns_policy(self):
        m = make_api_mock()
        args = {"siteId": "s1", "dnsPolicyId": "dp1", "type": "A_RECORD",
                "enabled": False, "domain": "updated.local"}
        run(dns, "update_dns_policy", args, m)
        m.assert_called_once_with("PUT", "/sites/s1/dns/policies/dp1",
                                  body={"type": "A_RECORD", "enabled": False,
                                        "domain": "updated.local"})

    def test_delete_dns_policy(self):
        m = make_api_mock()
        run(dns, "delete_dns_policy", {"siteId": "s1", "dnsPolicyId": "dp1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/dns/policies/dp1")


# ---------------------------------------------------------------------------
# Traffic
# ---------------------------------------------------------------------------

from tools import traffic

class TestTrafficDispatch:
    def test_list_traffic_matching_lists(self):
        m = make_api_mock()
        run(traffic, "list_traffic_matching_lists", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/traffic-matching-lists", params={})

    def test_get_traffic_matching_list(self):
        m = make_api_mock()
        run(traffic, "get_traffic_matching_list",
            {"siteId": "s1", "trafficMatchingListId": "tm1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/traffic-matching-lists/tm1")

    def test_create_traffic_matching_list(self):
        m = make_api_mock()
        args = {"siteId": "s1", "type": "PORTS", "name": "HTTP/S",
                "items": [{"portStart": 80, "portStop": 443}]}
        run(traffic, "create_traffic_matching_list", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert body["type"] == "PORTS"

    def test_update_traffic_matching_list(self):
        m = make_api_mock()
        args = {"siteId": "s1", "trafficMatchingListId": "tm1",
                "type": "IPV4_ADDRESSES", "name": "Printers",
                "items": [{"ipAddress": "10.0.0.10"}]}
        run(traffic, "update_traffic_matching_list", args, m)
        body = m.call_args.kwargs["body"]
        assert "siteId" not in body
        assert "trafficMatchingListId" not in body

    def test_delete_traffic_matching_list(self):
        m = make_api_mock()
        run(traffic, "delete_traffic_matching_list",
            {"siteId": "s1", "trafficMatchingListId": "tm1"}, m)
        m.assert_called_once_with("DELETE", "/sites/s1/traffic-matching-lists/tm1")


# ---------------------------------------------------------------------------
# Supporting
# ---------------------------------------------------------------------------

from tools import supporting

class TestSupportingDispatch:
    def test_list_wan_interfaces(self):
        m = make_api_mock()
        run(supporting, "list_wan_interfaces", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/wans", params={})

    def test_list_site_to_site_vpn_tunnels(self):
        m = make_api_mock()
        run(supporting, "list_site_to_site_vpn_tunnels", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/vpn/site-to-site-tunnels", params={})

    def test_list_vpn_servers(self):
        m = make_api_mock()
        run(supporting, "list_vpn_servers", {"siteId": "s1"}, m)
        m.assert_called_once_with("GET", "/sites/s1/vpn/servers", params={})
