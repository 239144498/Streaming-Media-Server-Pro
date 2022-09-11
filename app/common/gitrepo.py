#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
from urllib import parse
from base64 import b64encode

from app.modules.request import netreq


class agit:
    def __init__(self, access_token):
        self.headers = {
            "Host": "agit.ai",
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.access_token = access_token
        self.request = netreq()

    def get_file_sha(self, owner, repo, filepath, branch="master", i=0):
        if i > 10:
            raise Exception("无法获取sha")
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents/{parse.quote_plus(filepath)}?ref={branch}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            if res.status_code != 200:
                raise Exception(res.text)
            return res.json()['sha']

    def get_repo_sha(self, owner, repo, branch="master", i=0):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/git/refs/heads/{branch}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            if res.status_code != 200:
                raise Exception(res.text)
            return res.json()[-1]['object']['sha']

    def update_repo_file(self, owner, repo, filepath, content, branch="master", i=0):
        if i > 10:
            raise Exception("无法更新")
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "content": b64encode(content).decode(),
            "sha": self.get_file_sha(owner, repo, filepath)
        }
        with self.request.put(url=url, json=data, headers=self.headers) as res:
            return res.status_code

    def create_repo_file(self, owner, repo, filepath, content, branch="master", i=0):
        if i > 3:
            raise Exception("无法创建")
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "content": b64encode(content).decode(),
        }
        with self.request.post(url=url, json=data, headers=self.headers) as res:
            if res.status_code != 201:
                print(res.text)
                if res.status_code == 500:
                    return self.create_repo_file(owner, repo, filepath, content, i=i + 1)
            return res.status_code

    def delete_repo_file(self, owner, repo, filepath, branch="master", i=0):
        if i > 10:
            raise Exception("无法删除")
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "sha": self.get_file_sha(owner, repo, filepath)
        }
        with self.request.delete(url=url, json=data, headers=self.headers) as res:
            return res.status_code

    def create_branch(self, owner, repo, branch_name):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/branches?access_token={self.access_token}"
        data = {
            "new_branch_name": branch_name
        }
        with self.request.post(url=url, json=data, headers=self.headers) as res:
            return res.status_code

    def delete_branch(self, owner, repo, branch_name):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/branches/{branch_name}?access_token={self.access_token}"
        with self.request.delete(url=url, headers=self.headers) as res:
            return res.status_code

    def cat_branch(self, owner, repo):
        """
        查看所有分支
        :param owner:
        :param repo:
        :return:
        """
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/branches?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            return [i['name'] for i in res.json()]

    def cat_repo(self, owner, repo):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            return res.status_code

    def cat_repo_file_name(self, owner, repo, branchname="master"):
        """
        获取根目录的所有条目的元数据
        :param owner:
        :param repo:
        :return:
        """
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents?ref={branchname}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            return res.json()

    def cat_repo_tree(self, owner, repo, reposha):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/git/trees/{reposha}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            return res.json()

    def get_single_file_state(self, owner, repo, filename, branchname="master"):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}/contents/{filename}?ref={branchname}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers) as res:
            return res.status_code

    def create_repo(self, name):
        url = f"https://agit.ai/api/v1/user/repos?access_token={self.access_token}"
        data = {
            "auto_init": True,
            "name": name,
            "private": False,
        }
        with self.request.post(url=url, json=data, headers=self.headers) as res:
            return res.status_code

    def delete_repo(self, owner, repo):
        url = f"https://agit.ai/api/v1/repos/{owner}/{repo}?access_token={self.access_token}"
        with self.request.delete(url=url, headers=self.headers) as res:
            return res.status_code


if __name__ == '__main__':
    import datetime

    repo = str(datetime.date.today())
    repoaccess_token = "5e06fxxxxxac2xxxxxxab0d2baefdxxxxx"
    a1 = agit(repoaccess_token).create_repo(repo)
