class ProgressBar:
    def printProgressBar (self, iteration, total, length = 100):
        """Progress bar implementation.

        Keyword Arguments:
            - iteration -- current iteration
            - total -- total number of iterations
            - length -- progress bar length

        """

        percent = ('{0:.1f}').format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = '█' * filledLength + '-' * (length - filledLength)
        print(f'Progress: |{bar}| {percent}% Complete', end = '\r')

        if iteration == total: 
            print()