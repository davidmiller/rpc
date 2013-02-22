from rpc import soap

def main():
    client = soap.Client('http://services.aonaware.com/DictService/DictService.asmx?WSDL')
    print client.Define('soap')

if __name__ == '__main__':
    main()
