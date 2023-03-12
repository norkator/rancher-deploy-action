import os
import sys
import requests


class DeployRancher:
    def __init__(
            self,
            rancher_access_key,
            rancher_secret_key,
            rancher_url_api,
            rancher_cluster_id,
            rancher_namespace_id,
            rancher_service_name,
            rancher_docker_image
    ):
        self.access_key = rancher_access_key
        self.secret_key = rancher_secret_key
        self.rancher_url_api = rancher_url_api
        self.rancher_cluster_id = rancher_cluster_id
        self.rancher_namespace_id = rancher_namespace_id
        self.service_name = rancher_service_name
        self.docker_image = rancher_docker_image
        self.rancher_deployment_path = ''
        self.rancher_namespace = ''
        self.rancher_workload_url_api = ''

    def deploy(self):
        rp = requests.get('{}/clusters/{}/projects'.format(self.rancher_url_api, self.rancher_cluster_id),
                          auth=(self.access_key, self.secret_key))
        projects = rp.json()
        for p in projects['data']:
            w_url = '{}/projects/{}/workloads'.format(self.rancher_url_api, p['id'])
            rw = requests.get(w_url, auth=(self.access_key, self.secret_key))
            workload = rw.json()
            for w in workload['data']:
                if w['name'] == self.service_name and w['namespaceId'] == self.rancher_namespace_id:
                    print('found target service', w['name'], 'from user given namespace', w['namespaceId'])
                    self.rancher_workload_url_api = w_url
                    self.rancher_deployment_path = w['links']['self']
                    self.rancher_namespace = w['namespaceId']
                    break
            if self.rancher_deployment_path != '':
                break

        request_get = requests.get(self.rancher_deployment_path, auth=(self.access_key, self.secret_key))
        response = request_get.json()
        response['containers'][0]['image'] = self.docker_image
        result = requests.post(
            self.rancher_deployment_path + '?action=redeploy', json=response,
            auth=(self.access_key, self.secret_key)
        )
        print('redeploy completed with status code', result.status_code)
        sys.exit(0)

        # if 'status' in response and response['status'] == 404:
        #     config = {
        #         "containers": [{
        #             "imagePullPolicy": "Always",
        #             "image": self.docker_image,
        #             "name": self.service_name,
        #         }],
        #         "namespaceId": self.rancher_namespace,
        #         "name": self.service_name
        #     }
        #     requests.post(self.rancher_workload_url_api, json=config, auth=(self.access_key, self.secret_key))
        # else:
        #     response['containers'][0]['image'] = self.docker_image
        #     result = requests.post(
        #         self.rancher_deployment_path + '?action=redeploy', json=response,
        #         auth=(self.access_key, self.secret_key)
        #     )
        #     print('completed with status code', result.status_code)
        # sys.exit(0)


def deploy_in_rancher(
        rancher_access_key,
        rancher_secret_key,
        rancher_url_api,
        rancher_cluster_id,
        rancher_namespace_id,
        rancher_service_name,
        rancher_docker_image
):
    deployment = DeployRancher(
        rancher_access_key,
        rancher_secret_key,
        rancher_url_api,
        rancher_cluster_id,
        rancher_namespace_id,
        rancher_service_name,
        rancher_docker_image
    )
    deployment.deploy()


if __name__ == '__main__':
    rancher_access_key = os.environ['RANCHER_ACCESS_KEY']
    rancher_secret_key = os.environ['RANCHER_SECRET_KEY']
    rancher_url_api = os.environ['RANCHER_URL_API']
    rancher_cluster_id = os.environ['RANCHER_CLUSTER_ID']
    rancher_namespace_id = os.environ['NAMESPACE_ID']
    rancher_service_name = os.environ['SERVICE_NAME']
    rancher_docker_image = os.environ['DOCKER_IMAGE']
    rancher_docker_image_latest = os.environ['DOCKER_IMAGE_LATEST']
    try:
        deploy_in_rancher(
            rancher_access_key,
            rancher_secret_key,
            rancher_url_api,
            rancher_cluster_id,
            rancher_namespace_id,
            rancher_service_name,
            rancher_docker_image
        )
        if rancher_docker_image_latest != None and rancher_docker_image_latest != "":
            deploy_in_rancher(
                rancher_access_key,
                rancher_secret_key,
                rancher_url_api,
                rancher_cluster_id,
                rancher_namespace_id,
                rancher_service_name,
                rancher_docker_image_latest
            )

    except Exception as e:
        print(e)
        sys.exit(1)
