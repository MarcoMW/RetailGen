# -*- coding: utf-8 -*-
import dataReader, dataWriter, analyzer, generator, evaluator

if __name__=="__main__":
    print("RetailGen v0.1 (type help for more info)")
    while(True):
        input_var = input("> ").split(" ")
        args = dict()
        for i in range(1, len(input_var)-1):
            if input_var[i][0] == '-':
                args[input_var[i][1:]] = input_var[i+1]
        if(input_var[0] == 'exit'):
            break
        elif(input_var[0] == 'help'):
            if len(input_var) == 1:
                print("Commands: analyze, generate, evaluate, subset, exit")
                print("Type help _command_ for more information")
            else:
                if(input_var[1] == 'analyze'):
                    print("Mandatory args:input, output")
                if(input_var[1] == 'generate'):
                    print("Mandatory args: input, output")
                    print("Optional args: size, randomUsers, randomOrders")
                if(input_var[1] == 'evaluate'):
                    print("Mandatory args: file1, file2")
                if(input_var[1] == 'subset'):
                    print("Mandatory args:input, output, size")
        elif(input_var[0] == 'analyze'):
            analyzer.analyze('../Data/'+args['input'],'../Data/'+args['output'])
        elif(input_var[0] == 'generate'):
            randomUsers = 'randomUsers' in args
            randomOrders = 'randomOrders' in args
            generator.generate('../Data/'+args['input'],'../Data/'+args['output'], int(args.get('size', -1)), randomUsers, randomOrders)
        elif(input_var[0] == 'evaluate'):
            e = evaluator.evaluator('../Data/'+args['file1'],'../Data/'+args['file2'])
        elif(input_var[0] == 'subset'):
            df = dataReader.readOrders('../Data/'+args['input'])
            subset_df = dataWriter.makeOrderSubset(df, int(args['size']))
            dataWriter.writeOrderFileRandom(subset_df, '../Data/'+args['output'])
        else:
            print("Commands: analyze, generate, evaluate, subset, exit")
            print("Type help _command_ for more information")