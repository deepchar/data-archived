{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter a filenamehy-Latn.json\n"
     ]
    }
   ],
   "source": [
    "import json\n",
    "#from pprint import pprint \n",
    "\n",
    "\n",
    "file = input('Enter a filename') # Enter a full name of the file with the extenstion\n",
    "path = 'mappings\\\\' + file\n",
    "with open(path) as m:\n",
    "\tmapping = json.load(m)\n",
    "    \n",
    "#pprint(mapping)\n",
    "# uncomment in case you want to print the mapping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
