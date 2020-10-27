from application import app
import sys
import os

def main(port):
    app.run(debug=True,host='0.0.0.0',port=port)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'migration':
            os.system('python3 ./application/models/model.py')
        elif sys.argv[1] == '-port':
            main(int(sys.argv[2]))
        else:
            main(5000)
    except:
        main(5000)