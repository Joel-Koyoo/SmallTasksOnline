/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
 const colors = require('tailwindcss/colors')


 module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',
        './components/**/*.{html,js}',
        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        screens:{
            sm:'480px',
            md:'768px',
            lg:'976px',
            xl:'1440px'
          },
        extend: {
            colors:{
                Red: 'hsl(0, 100%, 50%)',
                brightRed: '#1434A4',
                brightRedLight: 'hsl(12,88%,69%)',
                brightRedSupLight: 'hsl(12,88%,95%)',
                darkBlue: 'hsl(228,39%,23%)',
                darkGrayishBlue: 'hsl(227,12%,61%)',
                veryDarkBlue: 'hsl(223,12%,13%)',
                veryPaleRed: 'hsl(13,100%,96%)',
                veryLightGray: 'hsl(0,0%,98%)',
                blue: '#0047AB',	
                white:' #fff',
                grey: '#f5f5f5',
                black1: '#222',
                black2:' #999',
                'cyan':colors.cyan,
                'teal':colors.teal
                
              }
        
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    
    ],
}
