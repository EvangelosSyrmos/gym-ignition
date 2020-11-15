# Copyright (C) 2020 Istituto Italiano di Tecnologia (IIT). All rights reserved.
# This software may be modified and distributed under the terms of the
# GNU Lesser General Public License v2.1 or any later version.

import abc
import gym_ignition.base.task


class PhysicsRandomizer(abc.ABC):
    """
    Abstract class that provides the machinery for randomizing the physics of a Task.

    Args:
        randomize_after_rollouts_num: defines after many rollouts physics should be
        randomized (i.e. the amount of times :py:meth:`gym.Env.reset` is called).
    """

    def __init__(self, randomize_after_rollouts_num: int = 0):

        self._rollout_counter = randomize_after_rollouts_num
        self.randomize_after_rollouts_num = randomize_after_rollouts_num

    @abc.abstractmethod
    def randomize_physics(self, task: gym_ignition.base.task.Task) -> None:
        """
        Method that insert and configures the physics of a Task's world.

        By default this method loads a plugin that uses DART with no randomizations.
        Randomizing physics engine parameters or changing physics engine backend could be
        done by redefining this method and passing it to
        :py:class:`~gym_ignition.runtimes.gazebo_runtime.GazeboRuntime`.

        Args:
            task: A task containing a world object without physics.
        """
        pass

    def increase_rollout_counter(self) -> None:
        """
        Increase the rollouts counter.
        """

        if self.randomize_after_rollouts_num != 0:
            assert self._rollout_counter != 0
            self._rollout_counter -= 1

    def physics_expired(self) -> bool:
        """
        Checks if the physics needs to be randomized.

        Return:
            True if the physics has expired, false otherwise.
        """

        if self.randomize_after_rollouts_num == 0:
            return False

        if self._rollout_counter == 0:
            self._rollout_counter = self.randomize_after_rollouts_num
            return True

        return False
