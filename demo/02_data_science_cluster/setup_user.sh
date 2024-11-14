#!/bin/bash

ADMINS="oaiadmin"
USERS="user1 user2"
PASSFILE=passfile
SECRET_NAME=htpass-secret
touch $PASSFILE


# --------------------------------------------------
# CREATE USERS 

for user in `echo $ADMINS $USERS`; do
    htpasswd -b $PASSFILE $user openshift
done

oc create secret generic $SECRET_NAME --from-file=htpasswd=$PASSFILE -n openshift-config

cat <<EOF | oc apply -f -
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: my_htpasswd_provider 
    mappingMethod: claim 
    type: HTPasswd
    htpasswd:
      fileData:
        name: $SECRET_NAME 
EOF

# --------------------------------------------------
# CREATE GROUPS 

cat <<EOF | oc apply -f -
apiVersion: user.openshift.io/v1
kind: Group
metadata:
  name: oai-users
users:
  - user1
  - user2
EOF

cat <<EOF | oc apply -f -
apiVersion: user.openshift.io/v1
kind: Group
metadata:
  name: oai-admins
users:
  - oaiadmin
EOF

# --------------------------------------------------
# ROLEBINDINGS 

oc adm policy add-cluster-role-to-group cluster-admin oai-admins
