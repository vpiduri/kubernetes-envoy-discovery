import json
import pytest
import responses


class TestExternalResource():
    """Functional tests for CastersResource."""

    @pytest.fixture
    def url(self):
        return '/v1/listeners/'

    #################
    # Test for GET. #
    #################

    @responses.activate
    def test_sensitive_data_is_not_in_account_response(self, app, k8s_endpoint_responses, k8s_service_response, url):
        responses.add(responses.GET, 'http://localhost:8001/api/v1/services',
                      json=k8s_service_response, status=200)
        responses.add(responses.GET,
                      'http://localhost:8001/api/v1/namespaces/kube-system/endpoints/kubernetes-dashboard',
                      json=k8s_endpoint_responses['kubernetes-dashboard'], status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/kube-system/endpoints/kube-dns',
                      json=k8s_endpoint_responses['kube-dns'], status=200)
        responses.add(responses.GET, 'http://localhost:8001/api/v1/namespaces/default/endpoints/kubernetes',
                      json=k8s_endpoint_responses['kubernetes'], status=200)
        response = app.get(url)
        response_data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert response_data is not None
        assert len(response_data['listeners']) == 3
        assert sorted(['kubernetes_8443',
                       'kube-dns_53',
                       'kubernetes-dashboard_9090']) == sorted([filter['name']
                                                                for listener in response_data['listeners']
                                                                for filter in listener['filters']])
