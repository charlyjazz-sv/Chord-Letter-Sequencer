import argparse

from trainer import OCRTrainer


def non_or_str(value):
    if value == None:
        return None
    return value

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OCR using CNN+RNN+CTC')
    parser.add_argument('--resume', type=non_or_str, help='resume from a checkpoint')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--eval', default=False, action='store_true', help='perform evaluation of trained model')
    parser.add_argument('--batch_size', type=int, default=16)
    
    args = parser.parse_args()    



    trainer = OCRTrainer(args)
    if args.eval:
        trainer.eval()
    else:
        trainer.train()






