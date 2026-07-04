#ifndef PING_PONG_BUF_H
#define PING_PONG_BUF_H

#include "pico/sem.h"

template <typename T, size_t BlockSize>
class PingPongBuffer {
private:
    T buffer[2][BlockSize];
    size_t write_idx;
    size_t frame_count;
    size_t read_idx;

    semaphore_t sem_block_ready;
    semaphore_t sem_block_free;

public: 
    void init() {
        write_idx = 0;
        frame_count = 0;
        read_idx = 0;

        sem_init(&sem_block_ready, 0, 0);
        sem_init(&sem_block_free, 0, 1);
    }

    void push(const T& frame) {
        buffer[write_idx][frame_count] = frame;
        frame_count++;

        if (frame_count == BlockSize) {
            write_idx = (write_idx + 1) % 2;
            frame_count = 0;

            sem_release(&sem_block_ready);
            sem_acquire_blocking(&sem_block_free);
        }
    }

    T* wait_for_full_block() {
        sem_acquire_blocking(&sem_block_ready);
        read_idx = (write_idx + 1) % 2;
        return buffer[read_idx];
    }
    void free_block() {
        sem_release(&sem_block_free);
    }
};

#endif  