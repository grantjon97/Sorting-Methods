# sorts.py
# Jonathan Grant
# 2016.01.22
# This program generates 100 random numbers into a Sorting_array class
# and sorts them using the quicksort method.

from csarray import Array
import random

# Constants
RANGE_LOW = 1
RANGE_HIGH = 20
LENGTH_OF_ARRAY = 100
COLUMNS_PER_ROW = 10
ARRAY_SIZE_LIST = [1, 3, 97, 501, 679]

class Sorting_array(Array):
    """ Defines methods for manipulating an array, specifically
    sorting it.
    """

    def __init__(self,size,default_value=None):
        """ Uses the initialization function of Array. """

       	super().__init__(size,default_value)

    def fill_random(self,low,high):
        """ Fills the array with random numbers.

        Parameters:
	LOW -- Lowest random number that can be generated
	HIGH -- Highest random number that can be generated
	"""

        for i in range(self.size):

            # HIGH + 1 is used because the number in the
            # argument for the largest possible random number
            # is excluded.
            self.data[i] = random.randrange(RANGE_LOW, RANGE_HIGH + 1)

    def fill_in_order(self):
        """ Fills the array in increasing order.

        The lowest and first number is 1, and the highest and
        last number in the array is the size of the array.
        """

        for i in range(0, self.size):
            self.data[i] = i + 1

    def fill_almost_in_order(self):
        """ Fills the array to almost perfectly increasing order.

        Calls the fill_in_order function, then swaps the first and
        last values of the array.
        """

        self.fill_in_order()

        # Swap the first and last boxes of the array.
        self.data[0], self.data[self.size - 1] = (self.data[self.size - 1],
                                                 self.data[0])

    def fill_reverse_order(self):
        """ Fills the array in decreasing order.

        The lowest and last number is 1, the highest and first number
        is equal to self.size.
        """

        for i in range(0, self.size):
            self.data[i] = self.size - i

    def fill_same_numbers(self):
        """ Fills the array with all of the same number."""

        for i in range(0, self.size):
            self.data[i] = 0

    def fill_array(self, fill_method):
        """ Fills the array with specified fill method.

        fill_method - integer that decides which fill method to use.
        """

        # Decide which fill method to use on the array
        if fill_method == 0:
            self.fill_random(RANGE_LOW, RANGE_HIGH)

        elif fill_method == 1:
            self.fill_in_order()

        elif fill_method == 2:
            self.fill_almost_in_order()

        elif fill_method == 3:
            self.fill_reverse_order()
        else:
            self.fill_same_numbers()


    def insertion_sort(self, h = 1):
        """ Sorts the array.

        Array is sorted in increasing order using the insertion
        sort method.

        h: Increment used to differentiate between insertion
           and Shell sort.

           Note: When using insertion sort, h will remain one.
                 Any higher increment would result
                 in the Shell sort.

        Source: Algorithms, R Sedgewick, Addison Wesley, 1988,
                pp 98-100
	"""

        for i in range(1, self.size):
            j = i
            key = self.data[j]
            while j > h - 1 and self.data[j - h] > key:
                self.data[j] = self.data[j - h]
                j = j - h
            self.data[j] = key

    def shellsort(self):
        """ Sorts the array from lowest to highest using an
        increment h.

        Source: Algorithms, R Sedgewick, Addison Wesley, 1988,
                pp 107-110
        """

        h = 1

        # Find the largest increment that can be used
        # with the array size. Note that the increment will
        # be greater than or equal to the size of the array here.
        while h < self.size:
            h = 3*h + 1

        # The increment is decreased first so that the largest
        # possible increment is used, without being greater than
        # or equal to the size of the array.
        while h > 1:
            h = (h-1) // 3
            self.insertion_sort(h)

    def downheap(self, k, n):
        """ Makes a heap.

        Points to the left child first, then figures out if there
        is a right child. If there is a right child, the two
        children are compared. The bigger child is then compared
        with its parent.

        k: The location of the parent
        n: The size of the array/tree
        """

        # is_heap: Boolean that shows whether the subtree is a heap
        # key: Holds the value of the parent

        is_heap = False
        key = self.data[k]

        # Compare parents to its children while the tree is
        # not a heap and there are still parents that have not
        # been compared
        while (not is_heap and k <= (n-2) // 2):
            if (n > 1):

                # Point to left child
                j = 2 * k + 1

                # Look for a right child, compare it with the
                # left child
                if (j + 1 < n):
                    if (self.data[j + 1] > self.data[j]):
                        j = j + 1

                # Subtree is a heap if the parent is larger
                # than its largest child
                if (key >= self.data[j]):
                    is_heap = True

                # If it isn't, switch the parent and child
                else:
                    self.data[k] = self.data[j]
                    k = j

            self.data[k] = key

    def heap_sort(self):
        """ Sort the array using heaps.

        Find the largest number in the tree, then decrease the size
        of the array by one.  Repeat until the tree has been reduced
        to a single number.

        Source: Algorithms, R Sedgewick, Addison Wesley, 1988,
                pp 148-161
        """
        # k: index used to point to each parent in the tree
        # n: size of the array
        # m: last element in the array

        n = self.size

        # Make an initial heap by pointing to the first parent
        # found in the tree.
        for k in range((n-2) // 2, -1, -1):
            self.downheap(k, n)

        # Note that downheap starts at the root
        # of the tree after making the initial heap.
        for m in range(n - 1, 0 , -1):
            self.data[0], self.data[m] = self.data[m], self.data[0]
            self.downheap(0, m)

    def partition(self, left, right):
        """ Partitions the array.

        Compares elements of the array with the first element,
        known as the pivot. Elements that are less than the pivot
        are switched to the left side of the pivot, while elements
        greater than or equal to the pivot are switched
        to the right side.

        left: The leftmost location in the array to be partitioned.

        right: The last location in the array to be partitioned.

        Source: Introduction to Algorithms, T Corman, C Leiserson,
                R Rivest, McGraw Hill, 1990, pp 153-155
        """

        # pivot - Number which elements of the array are compared
        #         with, and are then moved accordingly.
        # i - Starts on left of array/subset, compared with pivot
        # j - Starts on right of array/subset, compared with pivot

        pivot = self.data[left]
        i = left
        j = right

        # While the left and right pointers do not cross,
        # compare elements of the array with the pivot.
        while (i <= j):

            # Compare left pointer with pivot. As long as the
            # value at the pointer is less than the pivot, move the
            # pointer to the right.
            while (self.data[i] < pivot):
                i = i + 1

            # Compare right pointer with pivot. As long as the
            # value at the pointer is greater than or equal to the
            # pivot, move the pointer to the left.
            while (self.data[j] > pivot):
                j = j - 1

            # Swap the left and right pointers if their
            # location in the array have not crossed.
            if (i <= j):

                self.data[j], self.data[i] = self.data[i], self.data[j]

                i = i + 1
                j = j - 1

        return i

    def quicksort_rec(self, left, right):
        """ Sorts the array recursively using the quicksort method.

        left: The leftmost location in the partition.
              This will start off as zero when the array
              has not been partitioned yet.

        right: The last location in the partition.
               This will start off as self.size - 1 when
               the array has not been partitioned yet.
        """

        # q - Receives the value of the location of the partition

        if (left < right):
            q = self.partition(left, right)
            self.quicksort_rec(left, q - 1)
            self.quicksort_rec(q, right)

    def quicksort(self):
        """ Sorts the array using quicksort.

        Acts as a recursive driver to initialize the recursive
        quicksort function.
        """

        self.quicksort_rec(0, self.size - 1)

    def do_sort(self, sorting_method):
        """ Sorts the array using specified sorting method.

        Sorting methods used:

                Insertion Sort
                Shellsort
                Heap Sort
                Quicksort

        soting_method - index used to decide which sort to use
        """

        # Decide which sorting method to use on the array.
        if sorting_method == 0:
            self.insertion_sort()

        elif sorting_method == 1:
            self.shellsort()

        elif sorting_method == 2:
            self.heap_sort()

        else:
            self.quicksort()

    def check_order(self, sum):
        """ Checks if the array is in order.

        Returns a string that states whether the array
        is in order or not.

        sum - sum of the squares of the original, unsorted array
        """

        # is_sorted - boolean describing if the array is in order.
        # i - index of the array
        # sorted_sum - sum of the squares of the new, sorted array

        is_sorted = True
        i = 0

        # Only check order if the array has
        # multiple numbers to check against each other.
        if self.size > 1:

            # Check if the array has constantly
            # increasing numbers
            while is_sorted and i < self.size - 1:

                if self.data[i + 1] < self.data[i]:
                    is_sorted = False

                i = i + 1

            # Check if the manipulated array
            # still has the same numbers before being sorted,
            # but only if the array passed the previous test.
            if is_sorted:

                sorted_sum = 0
                for i in range(0, self.size):
                    sorted_sum = sorted_sum + ((self.data[i])**2)

            # If the sum of the squares of the array
            # do not equal each other before/after sorting,
            # then the array does not contain the same numbers as
            # it originally did.
            if sorted_sum != sum:
                is_sorted = False


        return is_sorted

    def print(self, msg=None):
        """ Prints the array data in column format. """

        if msg:
            print()
            print(msg)
            print()

        for i in range(len(self.data)):
            print('{:6d}'.format(self.data[i]), end = '')
            if ((i + 1) % COLUMNS_PER_ROW == 0):
                print()

def do_insertion_sort():
    """ Performs the behaviors of the Sorting_array class. """

    array = Sorting_array(LENGTH_OF_ARRAY)
    array.fill_random(RANGE_LOW, RANGE_HIGH)
    print('\nInsertion sort')
    print('\nUnsorted array:\n')
    array.print()
    array.insertion_sort()
    print('\nSorted array:\n')
    array.print()
    print()

def do_shellsort():
    """ Performs the behaviors of the Sorting_array class. """

    array = Sorting_array(LENGTH_OF_ARRAY)
    array.fill_random(RANGE_LOW, RANGE_HIGH)
    print('\nShellsort')
    print('\nUnsorted array:\n')
    array.print()
    array.shellsort()
    print('\nSorted array:\n')
    array.print()
    print()

def do_heap_sort():
    """ Performs the behaviors of the Sorting_array class. """

    array = Sorting_array(LENGTH_OF_ARRAY)
    array.fill_random(RANGE_LOW, RANGE_HIGH)
    print('\nHeap sort')
    print('\nUnsorted array:\n')
    array.print()
    array.heap_sort()
    print('\nSorted array:\n')
    array.print()
    print()

def do_quicksort():
    """ Performs the behaviors of the Sorting_array class. """

    array = Sorting_array(LENGTH_OF_ARRAY)
    array.fill_random(RANGE_LOW, RANGE_HIGH)
    print('\nQuicksort')
    print('\nUnsorted array:\n')
    array.print()
    array.quicksort()
    print('\nSorted array:\n')
    array.print()
    print()

def print_result(order_result_str, sorting_method, array_size, fill_method):
    """ Displays the results of the sorting test.

    order_result - string that states if the sort worked
    sorting_method - index representing the sorting method used
    array_size - size of the array
    fill_method - index representing the fill method used
    """

    # sortng_method_str - String representation of the sorting method
    # fill_method_str - String representation of the fill method

    # Identify which sorting method to print
    if sorting_method == 0:
        sorting_method_str = 'Insertion sort'
    elif sorting_method == 1:
        sorting_method_str = 'Shellsort'
    elif sorting_method == 2:
        sorting_method_str = 'Heap sort'
    else:
        sorting_method_str = 'Quicksort'

    # Identify which fill method to print
    if fill_method == 0:
        fill_method_str = 'Random order'
    elif fill_method == 1:
        fill_method_str = 'In order'
    elif fill_method == 2:
        fill_method_str = 'Reverse order'
    elif fill_method == 3:
        fill_method_str = 'Almost in order'
    else:
        fill_method_str = 'All same numbers'

    print('{:>3s}{:>25s}{:15d}{:>25s}'.format(order_result_str,
                                       sorting_method_str,
                                       array_size, fill_method_str))

def print_header():
    """ Prints the header description for the program."""

    print()
    print('Sorts testing')
    print()
    print('This program evaluates four different')
    print('sorting methods, including:')
    print()
    print('Insertion Sort\nShellsort\nHeap Sort\nQuicksort')
    print()
    print('Each evaluation includes the sorting method,')
    print('whether it was successful, the array size, and')
    print('the method in which it was filled.')
    print()
    print('Pass/Fail      Sorting Method     ', end = '')
    print('Array Size              Fill Method')
    print('---------      --------------     ', end = '')
    print('----------              -----------')
    print()

def test_all_sorts():
    """ Performs all of the above sorting methods.

    Tests all of the sorting methods by testing different
    sizes and orders (specifically special cases) of the array.
    """

    # sorting_method - Index deciding which sorting method to use.
    # array_size - Integer belonging to the list of array sizes
    # fill_method - Index deciding which fill method to use.
    # sum - The sum of the squares of the original, unsorted array.
    # order_result - Boolean stating if the array was sorted
    # order_result_str - String version of order_result,
    #                    either 'Pass' or 'Fail'

    print_header()

    for sorting_method in range(0,4):

        for array_size in ARRAY_SIZE_LIST:

            for fill_method in range(0, 5):

                # Make an array of some size.
                array = Sorting_array(array_size)

                # Fill the array using specified fill method.
                array.fill_array(fill_method)

                # Find sum of the squares in the array.
                # Used to check if the sorted array has the
                # same numbers as the original.
                sum = 0
                for i in range(0, array_size):
                    sum = sum + ((array.data[i])**2)

                # Sort the array using specified sorting method.
                array.do_sort(sorting_method)

                # Check if it's in order.
                order_result = array.check_order(sum)
                if order_result == True:
                    order_result_str = 'Pass'
                else:
                    order_result_str = 'Fail'

                # Report if the array is in order.
                print_result(order_result_str, sorting_method,
                             array_size, fill_method)

    # Added to prevent command line
    # from interfering with program
    print()

def Main():
    test_all_sorts()

if __name__ == "__main__":
    Main()
