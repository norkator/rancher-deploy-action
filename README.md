# Action for GitHub to re deploy image in Rancher using Rancher API

This action redeploys existing service. It's handy for automated pipeline which is building app, creating container
image and when that updated container image is needed to be deployed.

## Environment variables

```yaml
RANCHER_ACCESS_KEY=
RANCHER_SECRET_KEY=
RANCHER_URL_API=https://<address>/v3
RANCHER_CLUSTER_ID=
NAMESPACE_ID=
SERVICE_NAME=
DOCKER_IMAGE=
DOCKER_IMAGE_LATEST=
```

`RANCHER_ACCESS_KEY` **Required** API Access key created in Rancher.  
`RANCHER_SECRET_KEY` **Required** API Secret key created in Rancher.  
`RANCHER_URL_API` **Required** API url of your rancher. Example https://server-address/v3.  
`RANCHER_CLUSTER_ID` **Required** Cluster id can be found from url
like `https://server-address/v3/dashboard/c/c-m-dsmw2q28/explorer#cluster-events` here cluster id is `c-m-dsmw2q28`
part.   
`NAMESPACE_ID` **Required** deploy action uses selected namespace id  
`SERVICE_NAME` **Required** Name of your service on Rancher cluster which you want deploy/redeploy.  
`DOCKER_IMAGE` **Required** URL of your docker image.    
`DOCKER_IMAGE_LATEST` **Optional** URL of your docker image including latest tag.

## Example usage

Example for GitHub actions workflow

```yaml
- name: Rancher Deploy
  uses: norkator/rancher-deploy-action@1.0.0
  env:
    RANCHER_ACCESS_KEY: ${{ secrets.RANCHER_ACCESS_KEY }}
    RANCHER_SECRET_KEY: ${{ secrets.RANCHER_SECRET_KEY }}
    RANCHER_URL_API: ${{ secrets.RANCHER_URL_API }}
    RANCHER_CLUSTER_ID: ${{ secrets.RANCHER_CLUSTER_ID }}
    NAMESPACE_ID: ${{ secrets.NAMESPACE_ID }}
    SERVICE_NAME: 'service-name'
    DOCKER_IMAGE: 'ghcr.io/xxxxxxx'
    DOCKER_IMAGE_LATEST: 'ghcr.io/xxxxxxx:latest'
```

## Semantic Commit Messages

Origin [here](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716#file-semantic-commit-messages-md)

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

More Examples:

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)
