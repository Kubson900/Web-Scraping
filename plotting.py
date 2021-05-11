import matplotlib.pyplot as plt

class Plot:
    def __init__(self, product):
        self.product = product

    def plot_and_save_prices(self):
        fig, ax = plt.subplots()
        plt.title(self.product.name)
        plt.xlabel('Price')
        plt.ylabel('No. of products')
        _, cheap, expensive, common, _ = self.product.info
        text = '\n'.join([f'Min: {cheap[0][1]} zł', f'Max: {expensive[0][1]} zł', f'Most: {common[0][0]} zł'])
        ax.hist(self.product.prices, color='#2cbdfe', edgecolor='#36b0f8')
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.98, 0.85, text, transform=ax.transAxes, fontsize=9, ha='right', bbox=props)

        plt.savefig(f'Products/{self.product.name}/{self.product.name}_prices_histogram.png', bbox_inches='tight')
        plt.show()
