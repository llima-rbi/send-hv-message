# coding=utf-8
import argparse
import json
from os.path import isfile

import requests
from typing import Optional

from ui import AppUI, StoresLoaderUI


def main(config_data=None, stores_info=None):
    app = AppUI(defaults=config_data, stores_info=stores_info)
    app.master.title('Send HV Message')
    app.master.lift()
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()


def load_config():
    # type: () -> Optional[dict]
    parser = argparse.ArgumentParser(description='Envia mensagem para algum HV remoto.')
    parser.add_argument('config', help='arquivo de valores padrão (padrão: "./defaults.json"',
                        default='./defaults.json', nargs='?')
    args = parser.parse_args()
    config_path = args.config

    if not isfile(config_path):
        print 'Arquivo de padrões "{}" não encontrado.'.format(args.config)
        config_path = './defaults.json'

    if not isfile(config_path):
        print 'Arquivo de padrões "{}" não encontrado.'.format(args.config)
    else:
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except IOError:
            print 'Erro ao carregar valores padrão de "{}".'.format(config_path)
    return None


STORES_URL = 'http://bkmenuboard.e-deploy.com.br/StoreList'


def load_stores():
    try:
        return requests.get(STORES_URL).json()
    except:
        return None


def fetch_stores():
    stores = []

    def end_loading():
        stores.extend(load_stores())
        loading_ui.master.destroy()

    loading_ui = StoresLoaderUI()
    loading_ui.master.title('Carregando...')
    loading_ui.after(200, end_loading)
    loading_ui.master.lift()
    loading_ui.mainloop()
    return stores


if __name__ == '__main__':
    config = load_config()
    stores = None
    if config and config.get('fetch_stores'):
        stores = fetch_stores()
    main(config, stores)
