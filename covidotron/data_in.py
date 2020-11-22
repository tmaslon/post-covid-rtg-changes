from keras.preprocessing import image

#Funkcja tworzy generator konwertujący obrazy zapisane na dysku w tensory przygotowane do skierowania do sieci neuronowej
#Parametry:
#	- directory - ścieżka do folderu z obrazami
#	- target - docelowy rozmiar obrazu
#	- batch - wielkość pojedynczej paczki
#	- mode - sposób klasyfikacji obrazów (binary, categorical)
#Dodatkowo, piksele obrazów są odpowiednio przeskalowane, tj. znormalizowane do wartości z zakresu [0; 1].
#Dokładne wartości, jakie mogą przyjmować parametry target, batch i mode są określone wymogami obiekty ImageDataGenerator z biblioteki keras.
def data_as_tensors(directory,target,batch,mode):
	datagen = image.ImageDataGenerator(rescale=1./255)
	generator = datagen.flow_from_directory(directory, target_size=(target,target), batch_size=batch, class_mode=mode)
	return generator

#Funkcja dla augmentacji danych - można wykonywać tylko na zbiorze treningowym
#Wykonuje te same operacje, co funkcja data_as_tensors, lecz dodatkowo umożliwia wykonywania operacji na obrazach. Pozwala na generowanie w sposób losowych nowych obrazów na podstawie starych w celu sztucznego powiększania zbioru danych.
#Parametry:
#	- directory - ścieżka do folderu z obrazami
#	- target - docelowy rozmiar obrazu
#	- batch - wielkość pojedynczej paczki
#	- mode - sposób klasyfikacji obrazów (binary, categorical)
#	- rotation - zakres kątów, o które zostanie wykonany losowy obrót (0-180)
#	- width, height - ułamek całkowitej szerokości i wysokości obrazów; wskazują ramy, w których wykonuje się losowe przekształcenia w pionie i w poziomie
#	- shear - zakres losowego przycinania
#	- zoom - zakres losowego przybliżenia
#	- flip - losowe odbicie połowy obrazu w płaszczyźnie poziomej
#	- fill - strategia nowo utworzonych pikseli
#Parametry domyślne dla modyfikacji obrazów zostały wpisane przykładowo. Zachęca się do ich modyfikacji w dozwolonych ramach, określonych wymaganiami obiektu ImageDataGenerator z biblioteki keras.
def data_as_tensors_aug(directory,target,batch,mode,rotation=60,width=0.3,height=0.3,shear=0.1,zoom=0.1,flip=True,fill='nearest'):

	datagen = image.ImageDataGenerator(rescale=1./255,rotation_range=rotation,width_shift_range=width,height_shift_range=height,shear_range=shear,zoom_range=zoom,horizontal_flip=flip,fill_mode=fill)
	generator = datagen.flow_from_directory(directory, target_size=(target,target), batch_size=batch, class_mode=mode)
	return generator
	
#Przkeazuje dane w postaci pojdynczego tensora, nie generatora
#	directory - ścieżka do folderu z obrazami
#	files_number - pierwszy wymiar tensora (ilość próbek)
#	target_size - rozmiar obrazu, do którego zostaną przekształcone dane wejściowe (drugi i trzeci wymiar tensora)
#	class_mode - sposób klasyfikacji obrazu (binary,categorical)
def data_as_tensors_vectorize(directory,files_number,target_size,class_mode):
	data_generator = data_as_tensors(directory,target_size,files_number,class_mode)
	for data_batch, labels_batch in data_generator:
		data = data_batch
		labels = labels_batch
		break
	return data,labels
