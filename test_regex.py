import re
html_bruto = '\n                      <div class="placa ng-binding">\n                        <span class="iconSne-placa"></span> ABC123\n                      </div>\n                      <div class="renavam ng-binding">\n                        <span class="iconSne-veiculo02"></span> 12345689\n                      </div>\n                    '
html_sem_espacos = re.sub(r'\s', '', html_bruto)
placa, renavan = re.search('</span>(\w+)</div>.+</span>(\w+)</div>', html_sem_espacos, re.IGNORECASE).groups()
print(placa, renavan)