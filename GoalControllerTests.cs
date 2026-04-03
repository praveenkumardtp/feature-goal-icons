using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Xunit;
using Moq;
using Microsoft.AspNetCore.Mvc;

using commbank.Controllers;
using commbank.Models;
using commbank.Services;

namespace commbank.Tests
{
    public class GoalControllerTests
    {
        private readonly Mock<IGoalService> _goalServiceMock;
        private readonly GoalController _controller;

        public GoalControllerTests()
        {
            _goalServiceMock = new Mock<IGoalService>();
            _controller = new GoalController(_goalServiceMock.Object);
        }

        [Fact]
        public async Task GetGoalsForUser_ReturnsOk_WithGoals()
        {
            // Arrange
            var userId = "user-1";

            var goals = new List<Goal>
            {
                new Goal { Id = "1", Title = "Learn React", Icon = "📘" },
                new Goal { Id = "2", Title = "Build Project", Icon = "🚀" }
            };

            _goalServiceMock
                .Setup(service => service.GetGoalsForUser(userId))
                .ReturnsAsync(goals);

            // Act
            var result = await _controller.GetGoalsForUser(userId);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedGoals = Assert.IsType<List<Goal>>(okResult.Value);

            Assert.Equal(2, returnedGoals.Count);
        }

        [Fact]
        public async Task GetGoalsForUser_ReturnsEmptyList_WhenNoGoals()
        {
            // Arrange
            var userId = "user-2";

            _goalServiceMock
                .Setup(service => service.GetGoalsForUser(userId))
                .ReturnsAsync(new List<Goal>());

            // Act
            var result = await _controller.GetGoalsForUser(userId);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnedGoals = Assert.IsType<List<Goal>>(okResult.Value);

            Assert.Empty(returnedGoals);
        }

        [Fact]
        public async Task GetGoalsForUser_ReturnsBadRequest_WhenUserIdIsNull()
        {
            // Act
            var result = await _controller.GetGoalsForUser(null);

            // Assert
            Assert.IsType<BadRequestResult>(result);
        }

        [Fact]
        public async Task GetGoalsForUser_ReturnsBadRequest_WhenUserIdIsEmpty()
        {
            // Act
            var result = await _controller.GetGoalsForUser("");

            // Assert
            Assert.IsType<BadRequestResult>(result);
        }
    }
}