import numpy as np


def auto_corr2D_viafft(data, normalize=True, rescale=False):

    # Returns a 2D autocorrelation computed via an intermediate FFT

    # Number of data pts
    nx, ny = data.shape[0], data.shape[1]

    padded = np.append(data, np.zeros((nx,ny)), axis=0)
    padded = np.append(padded, np.zeros((2*nx,ny)), axis=1)

    # Perform the FFT
    data_dft = np.fft.fft2(padded)

    # DFT of auto-correlation is simply (conjugate) multiplication
    # Elt-wise multiplication of fft
    data_ac_dft = np.multiply(np.conjugate(data_dft), data_dft)

    # Inverse FFT to return to time
    # Note this array will be half-shifted
    result_shifted = np.real(np.fft.ifft2(data_ac_dft))

    # Flip the result array around
    return_shape = (result_shifted.shape[0]-1, result_shifted.shape[1]-1)
    temp_array_a = np.empty(return_shape, dtype=float)
    temp_array_b = np.empty(return_shape, dtype=float)

    # Flip in x:
    temp_array_a[0:nx, :] = result_shifted[nx-1:2*nx-1, 0:2*ny-1]
    temp_array_a[nx:2*nx-1, :] = result_shifted[0:nx-1, 0:2*ny-1]
    # Flip in y:
    temp_array_b[:, 0:ny] = temp_array_a[:, ny-1:2*ny-1]
    temp_array_b[:, ny:2*ny-1] = temp_array_a[:, 0:ny-1]

    # Compensate for the size of integration overlap
    if rescale:
        rows = return_shape[0]
        cols = return_shape[1]
        for row in range(0, rows):
            rowcount = nx - np.abs(row + 1 - nx)
            for col in range(0, cols):
                colcount = ny - np.abs(col + 1 - ny)
                scalar = 1. / (float(rowcount) * float(colcount))
                temp_array_b[row, col] *= scalar

    if normalize:
        return temp_array_b/float(nx*ny)
    else:
        return temp_array_b


def twoD_Gaussian(x_y, os, amplitude, sig_x, sig_y, theta):
    # First back-rotate the points
    x, y = x_y
    (xrot, yrot) = (x * np.cos(theta) + y * np.sin(theta),
                    y * np.cos(theta) - x * np.sin(theta))

    # Now compute relative to an xy-aligned gaussian
    g = os + amplitude * np.exp(-(xrot/sig_x)**2 - (yrot/sig_y)**2)

    # Flatten the result
    return g.ravel()
