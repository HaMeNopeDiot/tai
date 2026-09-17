from openai import OpenAI
import subprocess
import argparse
import json
from pathlib import Path

from tools.config_data import ConfigData
from tools.dump   import Dumper

def prepare_chat_request(args):
    user_text = {"role": "user", "content": args.request_text}
    if args.prev_msg != "":
        with open(args.prev_msg, 'r', encoding='utf-8') as f:
            content = f.read()
        msg = [
            {"role": "system", "content": "Ты полезный помощник."},
            user_text,
            {"role": "assistant", "content": content},
        ]
    elif args.topic != "":
        try:
            filename = Path("topics") / f"{args.topic}.json"
            with open(filename, 'r', encoding='utf-8') as f:
                msg = json.load(f)
            msg.append(user_text)
        except FileNotFoundError:
            with open(filename, 'w', encoding='utf-8') as f:
                pass
            msg = [
                {"role": "system", "content": "Ты полезный помощник."},
                user_text,
            ]
    else:
        msg = [
            {"role": "system", "content": "Ты полезный помощник."},
            user_text,
        ]
    return msg

def parser_enable():
    # parse section
    parser = argparse.ArgumentParser(description="Terminal access to chat with AI")
    parser.add_argument("-m", "--msg",   dest="request_text",   type=str,             help="Your request")
    parser.add_argument("-p", "--pmsg",  dest="prev_msg",       type=str, default="", help="Prev msg in .md format")
    parser.add_argument("-t", "--topic", dest="topic",          type=str, default="", help="Topic name file")
    args = parser.parse_args()
    return args



def glow_md(filename: str):
    try:
        # Использование ["glow", filename] безопасно и передает файл аргументом
        subprocess.run(["glow", filename])
    except FileNotFoundError:
        print("No 'glow' installed.")


if __name__ == "__main__":
    args = parser_enable()

    dagent  = Dumper()
    cfgdata = ConfigData()
    cfgdata.parse_config()

    client = OpenAI(
        api_key=cfgdata.api_key,
        base_url=cfgdata.base_url
    )

    msg = prepare_chat_request(args)

    # main part
    # ------------------------------------------------------------------------ #
    response = client.chat.completions.create(
        model=cfgdata.model,
        messages=msg,
        temperature=cfgdata.temperature,
    )

    content = response.choices[0].message.content
    msg.append({"role": "assistant", "content": content})


    dagent.dump_json(args.topic, msg)
    ufilename = dagent.dump_md(args.topic, content)
    glow_md(ufilename)