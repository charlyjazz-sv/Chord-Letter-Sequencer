import argparse

from trainer import OCRTrainer


def non_or_str(value):
    if value == None:
        return None
    return value

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OCR using CNN+RNN+CTC')
    parser.add_argument('--resume', type=non_or_str, help='resume from a checkpoint')
    parser.add_argument('--dataset', type=non_or_str, default="./chord_train",help='dataset for training/evaluation')
    parser.add_argument('--epochs', type=int, default=500, help='Number of epochs')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning Rate')
    parser.add_argument('--eval', default=False, action='store_true', help='perform evaluation of trained model for display')
    parser.add_argument('--eval_chords', default=False, action='store_true', help='perform evaluation of trained model for accuracy')
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--interval', type=int, default=150)
    parser.add_argument('--eval_img', type=non_or_str,help='Predict on single image')
    
    args = parser.parse_args()    



    trainer = OCRTrainer(args)
    if args.eval:
        trainer.eval()
    elif args.eval_chords:
        trainer.eval_chords()
    elif args.eval_img is not None:
        trainer.eval_img(args.eval_img)
    else:
        trainer.train()






