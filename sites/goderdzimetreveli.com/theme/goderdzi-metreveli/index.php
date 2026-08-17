<?php
/**
 * Required fallback. archive.php handles every listing view this site uses.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_template_part( 'archive' );
