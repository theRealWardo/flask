module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    watch: {
      dev: {
        files: ['js/*.js', 'js/**/*.js', 'css/*.css', 'css/**/*.css'],
        tasks: ['default', 'cssmin'],
        options: {
          spawn: false,
          livereload: 2222,
        },
      },
    },
    ngtemplates: {
      all: {
        src: 'templates/*.html',
        dest: 'build/templates.js',
        options: {
          htmlmin: {
            collapseWhitespace: true,
            collapseBooleanAttributes: true,
          }
        }
      }
    },
    concat: {
      build: {
        src: ['js/**/*.js', 'js/*.js'],
        dest: 'build/<%= pkg.name %>.js',
      },
      dist: {
        src: ['js/*.js', 'js/**/*.js', 'build/templates.js'],
        dest: 'build/<%= pkg.name %>-tmpl.js',
      },
    },
    uglify: {
      build: {
        src: 'build/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      },
      dist: {
        src: 'build/<%= pkg.name %>-tmpl.js',
        dest: 'build/<%= pkg.name %>-tmpl.min.js'
      },
    },
    cssmin: {
      dist: {
        files: {
          'build/main.css': ['css/main.css']
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-angular-templates');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['concat:build', 'uglify:build']);
  grunt.registerTask('dist', ['ngtemplates', 'concat:dist', 'uglify:dist', 'cssmin']);
};
